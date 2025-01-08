import pytest
from playwright.sync_api import sync_playwright
import json
import os

BASE_URL = "http://127.0.0.1:7860/"  # Replace with the actual running URL of agentlab-xray


def start_playwright():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    return playwright, browser


def stop_playwright(playwright, browser):
    browser.close()
    playwright.stop()


@pytest.fixture(scope="module")
def browser():
    playwright, browser = start_playwright()
    yield browser
    stop_playwright(playwright, browser)


def load_mock_data():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(
        base_dir,
        "data",
        "test_study",
        "2024-08-01_10-20-52_GenericAgent_on_miniwob.ascending-numbers_64_e6d2d5",
        "summary_info.json",
    )
    with open(file_path, "r") as f:
        return json.load(f)


def test_data_loads_without_errors(browser):
    page = browser.new_page()
    page.goto(BASE_URL)

    page.wait_for_selector("input[aria-label='Experiment Directory']", timeout=3000)
    dropdown = page.locator("input[aria-label='Experiment Directory']")
    dropdown.click()
    page.wait_for_selector("ul[role='listbox']", timeout=2000)
    page.locator(
        "ul[role='listbox'] li:text('2024-08-01_10-20-52_GenericAgent_on_miniwob.ascending-numbers_64_e6d2d5')"
    ).click()
    assert page.wait_for_selector("#agent-table", timeout=3000), "Agent table did not load."
    page.click("text=Error Report")
    error_report = page.locator(".error-report").inner_text()
    assert (
        "No error report found" in error_report or not error_report.strip()
    ), "Errors were found in the error report."
    page.close()


def test_agent_selection(browser):
    page = browser.new_page()
    page.goto(BASE_URL)

    page.wait_for_selector("input[aria-label='Experiment Directory']", timeout=3000)
    dropdown = page.locator("input[aria-label='Experiment Directory']")
    dropdown.click()
    page.wait_for_selector("ul[role='listbox']", timeout=2000)
    page.locator(
        "ul[role='listbox'] li:text('2024-08-01_10-20-52_GenericAgent_on_miniwob.ascending-numbers_64_e6d2d5')"
    ).click()
    agent_table = page.locator("#agent-table")
    assert agent_table.is_visible(), "Agent table is not visible."
    agent_table.locator("tr").nth(1).click()
    task_table = page.locator("#task_table")
    seed_table = page.locator("#seed_table")
    assert task_table.is_visible(), "Task table did not load after selecting agent."
    assert seed_table.is_visible(), "Seed table did not load after selecting agent."
    page.close()


def test_profiling_tab_loads(browser):
    page = browser.new_page()
    page.goto(BASE_URL)

    page.wait_for_selector("input[aria-label='Experiment Directory']", timeout=3000)
    dropdown = page.locator("input[aria-label='Experiment Directory']")
    dropdown.click()
    page.wait_for_selector("ul[role='listbox']", timeout=2000)
    page.locator(
        "ul[role='listbox'] li:text('2024-08-01_10-20-52_GenericAgent_on_miniwob.ascending-numbers_64_e6d2d5')"
    ).click()
    page.locator("#agent-table tr").nth(1).click()
    page.locator("#task_table tr").nth(1).click()
    page.locator("#seed_table tr").nth(1).click()
    page.wait_for_selector("text=Profiling", timeout=2000)
    profiling_image = page.locator("text=Profiling")
    assert profiling_image.is_visible(), "Profiling tab did not load."
    page.close()
