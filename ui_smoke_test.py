from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:8000"
ARTIFACT_DIR = Path("artifacts")
ARTIFACT_DIR.mkdir(exist_ok=True)


def save(page, name):
    page.screenshot(path=str(ARTIFACT_DIR / name), full_page=True)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 首页
    page.goto(BASE_URL, wait_until="networkidle")
    save(page, "01_home.png")

    # 学生登录
    page.goto(f"{BASE_URL}/studentLogin/", wait_until="networkidle")
    page.fill("input[name='sid']", "123456")
    page.fill("input[name='password']", "123456")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    save(page, "02_student_login.png")

    # 尝试进入考试并交卷
    start_exam_links = page.locator("a:has-text('开始考试')")
    if start_exam_links.count() > 0:
        start_exam_links.first.click()
        page.wait_for_load_state("networkidle")
        save(page, "03_exam_page.png")

        first_radio = page.locator("input[type='radio']").first
        if first_radio.count() > 0:
            first_radio.check()
        submit = page.locator("button:has-text('提交试卷')")
        if submit.count() > 0:
            submit.click()
            page.wait_for_load_state("networkidle")
            save(page, "04_submit_exam.png")

    # 角色登录页可访问性检查
    for path, shot in [
        ("/admin_login/", "05_admin_login.png"),
        ("/staff_login/", "06_staff_login.png"),
        ("/teacher_login/", "07_teacher_login.png"),
    ]:
        page.goto(f"{BASE_URL}{path}", wait_until="networkidle")
        save(page, shot)

    browser.close()

print("UI smoke test finished.")
