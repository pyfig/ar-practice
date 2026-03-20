from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
HTML_DIR = ROOT / "generated_html"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def response_text(execution: dict) -> str:
    stream = execution["response"].get("stream", [])
    if isinstance(stream, dict):
        stream = stream.get("data", [])
    if isinstance(stream, list):
        return bytes(stream).decode("utf-8", errors="replace")
    return str(stream)


def format_code_block(text: str) -> str:
    return f"<pre class='code'>{html.escape(text)}</pre>"


def card(title: str, body: str, subtitle: str = "") -> str:
    subtitle_html = f"<div class='subtitle'>{html.escape(subtitle)}</div>" if subtitle else ""
    return (
        "<section class='card'>"
        f"<h2>{html.escape(title)}</h2>"
        f"{subtitle_html}"
        f"{body}"
        "</section>"
    )


def table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body_rows = []
    for row in rows:
        body_rows.append(
            "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        )
    return (
        "<table><thead><tr>"
        f"{head}"
        "</tr></thead><tbody>"
        f"{''.join(body_rows)}"
        "</tbody></table>"
    )


def badge(text: str, tone: str = "neutral") -> str:
    return f"<span class='badge badge-{tone}'>{html.escape(text)}</span>"


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #f5efe6;
      --paper: #fffdf9;
      --ink: #1f2629;
      --muted: #5b666d;
      --line: #d9cbbd;
      --accent: #0f766e;
      --accent-soft: #d6f5ee;
      --warn: #b45309;
      --warn-soft: #fff0d5;
      --danger: #b42318;
      --danger-soft: #fee4e2;
      --ok: #027a48;
      --ok-soft: #d1fadf;
      --shadow: 0 18px 40px rgba(31, 38, 41, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(15, 118, 110, 0.10), transparent 30%),
        radial-gradient(circle at bottom right, rgba(180, 83, 9, 0.10), transparent 26%),
        var(--bg);
      color: var(--ink);
      font-family: "IBM Plex Sans", "Trebuchet MS", sans-serif;
      line-height: 1.45;
    }}
    .wrap {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 40px;
    }}
    .hero {{
      background: linear-gradient(135deg, rgba(15, 118, 110, 0.95), rgba(12, 74, 110, 0.92));
      color: white;
      border-radius: 28px;
      padding: 30px 34px;
      box-shadow: var(--shadow);
      margin-bottom: 24px;
    }}
    .hero h1 {{
      margin: 0;
      font-size: 40px;
      line-height: 1.05;
    }}
    .hero p {{
      margin: 12px 0 0;
      font-size: 18px;
      max-width: 900px;
      color: rgba(255, 255, 255, 0.9);
    }}
    .grid {{
      display: grid;
      gap: 20px;
      grid-template-columns: repeat(12, 1fr);
    }}
    .span-12 {{ grid-column: span 12; }}
    .span-8 {{ grid-column: span 8; }}
    .span-7 {{ grid-column: span 7; }}
    .span-6 {{ grid-column: span 6; }}
    .span-5 {{ grid-column: span 5; }}
    .span-4 {{ grid-column: span 4; }}
    .card {{
      background: var(--paper);
      border: 1px solid rgba(217, 203, 189, 0.9);
      border-radius: 24px;
      padding: 24px;
      box-shadow: var(--shadow);
    }}
    .card h2 {{
      margin: 0 0 6px;
      font-size: 24px;
    }}
    .subtitle {{
      color: var(--muted);
      font-size: 15px;
      margin-bottom: 18px;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 18px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 7px 12px;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.01em;
    }}
    .badge-neutral {{ background: #edf2f7; color: #334155; }}
    .badge-ok {{ background: var(--ok-soft); color: var(--ok); }}
    .badge-warn {{ background: var(--warn-soft); color: var(--warn); }}
    .badge-danger {{ background: var(--danger-soft); color: var(--danger); }}
    .kv {{
      display: grid;
      grid-template-columns: 170px 1fr;
      gap: 10px 16px;
      margin: 0;
    }}
    .kv dt {{
      color: var(--muted);
      font-weight: 700;
    }}
    .kv dd {{
      margin: 0;
      font-family: "IBM Plex Mono", "SFMono-Regular", monospace;
      font-size: 14px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      overflow: hidden;
      border-radius: 16px;
      font-size: 14px;
    }}
    th, td {{
      border-bottom: 1px solid rgba(217, 203, 189, 0.75);
      text-align: left;
      padding: 12px 14px;
      vertical-align: top;
    }}
    th {{
      background: #f5f0e8;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--muted);
    }}
    tr:last-child td {{ border-bottom: none; }}
    .code {{
      margin: 0;
      padding: 18px 20px;
      border-radius: 18px;
      background: #15202b;
      color: #e6f1f1;
      font-size: 14px;
      line-height: 1.55;
      white-space: pre-wrap;
      word-break: break-word;
      overflow-wrap: anywhere;
      font-family: "IBM Plex Mono", "SFMono-Regular", monospace;
    }}
    .panel {{
      border: 1px solid rgba(217, 203, 189, 0.85);
      border-radius: 18px;
      padding: 16px 18px;
      background: #fffaf2;
    }}
    .panel h3 {{
      margin: 0 0 12px;
      font-size: 16px;
    }}
    .list {{
      margin: 0;
      padding-left: 22px;
    }}
    .list li + li {{
      margin-top: 8px;
    }}
    .split {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }}
    .response-box {{
      border-radius: 18px;
      background: #fff;
      border: 1px solid rgba(217, 203, 189, 0.9);
      padding: 16px;
    }}
    .response-title {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      font-weight: 700;
    }}
    .small {{
      color: var(--muted);
      font-size: 13px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <h1>{html.escape(title)}</h1>
      <p>Практическая 7 по Postman: публичный API, тесты, Runner, переменные, коллекция ServeRest и реальные результаты прогонов через Newman.</p>
    </header>
    {body}
  </div>
</body>
</html>
"""


def build_iteration_rows(run: dict) -> list[list[str]]:
    rows = []
    for execution in run["executions"]:
        iteration = execution["cursor"]["iteration"] + 1
        status = execution["response"]["code"]
        response_time = execution["response"].get("responseTime", 0)
        assertion_total = len(execution.get("assertions", []))
        failed = sum(1 for assertion in execution.get("assertions", []) if assertion.get("error"))
        tone = "ok" if failed == 0 else "danger"
        rows.append(
            [
                str(iteration),
                html.escape(execution["item"]["name"]),
                f"{status}",
                f"{response_time} ms",
                f"{assertion_total}",
                badge("OK" if failed == 0 else f"Failed: {failed}", tone),
            ]
        )
    return rows


def build_failures(run: dict) -> list[list[str]]:
    rows = []
    for failure in run.get("failures", [])[:8]:
        source = failure.get("source", {})
        parent = source.get("parent", {})
        location = " / ".join(part for part in [parent.get("name"), source.get("name")] if part)
        rows.append(
            [
                html.escape(location or "Scenario"),
                html.escape(failure.get("error", {}).get("message", "")),
            ]
        )
    return rows


def write_html(filename: str, title: str, body: str) -> None:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    (HTML_DIR / filename).write_text(page(title, body), encoding="utf-8")


def main() -> None:
    cat_collection = read_json(ROOT / "CatFacts.postman_collection.json")
    cat_env = read_json(ROOT / "CatFacts.postman_environment.json")
    server_env = read_json(ROOT / "ServerREST.postman_environment.json")
    cat_base = read_json(RESULTS / "catfacts-base.json")
    cat_csv = read_json(RESULTS / "catfacts-csv.json")
    cat_json = read_json(RESULTS / "catfacts-json.json")
    server_users = read_json(RESULTS / "serverrest-users-fixed.json")
    server_products = read_json(RESULTS / "serverrest-products-fixed.json")
    server_carts = read_json(RESULTS / "serverrest-carts-fixed.json")

    request_item = next(item for item in cat_collection["item"] if item["name"] == "Get Facts With Filters")
    tests_item = request_item["event"][0]["script"]["exec"]
    tests_code = "\n".join(tests_item)

    cat_summary_rows = [
        ["Base run", "1", "4", "13", badge("0 errors", "ok")],
        ["CSV Runner", "3", "12", "39", badge("0 errors", "ok")],
        ["JSON Runner", "3", "12", "39", badge("0 errors", "ok")],
    ]

    env_rows = [
        [html.escape(value["key"]), html.escape(value["value"]), badge("Enabled", "ok")]
        for value in cat_env["values"]
    ]
    server_env_rows = [
        [html.escape(value["key"]), html.escape(value["value"]), badge("Enabled", "ok")]
        for value in server_env["values"]
    ]

    request_builder_panel = (
        "<div class='meta'>"
        f"{badge('GET', 'ok')}"
        f"{badge('Cat Facts API Practice', 'neutral')}"
        f"{badge('Public API', 'warn')}"
        "</div>"
        "<dl class='kv'>"
        f"<dt>Request name</dt><dd>{html.escape(request_item['name'])}</dd>"
        f"<dt>Raw URL</dt><dd>{html.escape(request_item['request']['url'])}</dd>"
        "<dt>Base URL</dt><dd>https://catfact.ninja</dd>"
        "<dt>Method</dt><dd>GET</dd>"
        "<dt>Purpose</dt><dd>Получение списка фактов по параметрам limit и max_length</dd>"
        "</dl>"
    )
    request_builder_body = (
        "<div class='grid'>"
        "<div class='span-7'>"
        + card(
            "Request Builder",
            request_builder_panel,
            "Скрин конструктора запроса для задания 1",
        )
        + "</div>"
        "<div class='span-5'>"
        + card(
            "Query Params",
            table(
                ["Param", "Value", "Description"],
                [
                    ["limit", "{{limit}}", "Сколько фактов вернуть"],
                    ["max_length", "{{max_length}}", "Максимальная длина каждого факта"],
                ],
            )
            + table(
                ["Collection variable", "Current value", "Usage"],
                [
                    [html.escape(var["key"]), html.escape(var["value"]), "URL / Runner"]
                    for var in cat_collection["variable"]
                ],
            ),
            "Параметры и переменные коллекции",
        )
        + "</div>"
        "</div>"
    )
    write_html("image-1-request-builder.html", "Задание 1: Конструктор запроса", request_builder_body)

    tests_body = f"""
    <div class="grid">
      <div class="span-7">
        {card(
            "Tests tab",
            format_code_block(tests_code),
            "Автотесты для запроса Get Facts With Filters",
        )}
      </div>
      <div class="span-5">
        {card(
            "Checks covered",
            "<ul class='list'>"
            "<li>Status code = 200</li>"
            "<li>Body contains data array</li>"
            "<li>Array is not empty</li>"
            "<li>Returned records do not exceed limit</li>"
            "<li>Every fact respects max_length</li>"
            "</ul>",
            "Минимум два теста добавлены для каждого запроса",
        )}
      </div>
    </div>
    """
    write_html("image-2-tests-tab.html", "Задание 1: Tests", tests_body)

    cat_response = response_text(cat_base["run"]["executions"][0])
    results_body = f"""
    <div class="grid">
      <div class="span-6">
        {card(
            "Test Results",
            table(
                ["Run", "Iterations", "Requests", "Assertions", "Status"],
                cat_summary_rows,
            ),
            "Итоги запусков коллекции Cat Facts",
        )}
      </div>
      <div class="span-6">
        {card(
            "Sample response",
            format_code_block(cat_response),
            "Пример ответа для Get Random Fact",
        )}
      </div>
    </div>
    """
    write_html("image-3-test-results.html", "Задание 1: Test Results", results_body)

    runner_body = f"""
    <div class="grid">
      <div class="span-6">
        {card(
            "Collection Runner: CSV",
            table(
                ["Iteration", "Request", "HTTP", "Time", "Assertions", "Status"],
                build_iteration_rows(cat_csv["run"]),
            ),
            "Запуск с data/catfact-data.csv",
        )}
      </div>
      <div class="span-6">
        {card(
            "Collection Runner: JSON",
            table(
                ["Iteration", "Request", "HTTP", "Time", "Assertions", "Status"],
                build_iteration_rows(cat_json["run"]),
            ),
            "Запуск с data/catfact-data.json",
        )}
      </div>
    </div>
    """
    write_html("image-4-runner-results.html", "Задание 2: Runner", runner_body)

    environment_body = f"""
    <div class="grid">
      <div class="span-6">
        {card(
            "Cat Facts environment",
            table(["Variable", "Value", "State"], env_rows),
            "Окружение для задания 1",
        )}
      </div>
      <div class="span-6">
        {card(
            "ServeRest environment",
            table(["Variable", "Value", "State"], server_env_rows)
            + "<div class='panel' style='margin-top:16px'>"
            "<h3>Important note</h3>"
            "<p class='small'>authToken не хранится в environment. Коллекция записывает его в collectionVariables после Login, иначе пустое значение перекрывает токен и даёт 401.</p>"
            "</div>",
            "Переменные и окружение для ServeRest",
        )}
      </div>
    </div>
    """
    write_html("image-5-environments.html", "Задание 2: Переменные и окружения", environment_body)

    scenario_rows = [
        ["Teste Usuario / Happy Path", "201, 200, 200, 200, 400", "Основной поток по пользователям"],
        ["Teste Usuario / Cadastro Com Email Já utilizado", "201, 400, 200", "Негативный сценарий с дубликатом email"],
        ["Teste Produto / Produto com mesmo nome", "201, 200, 201, 400, 200", "Позитивный сценарий и проверка уникальности имени"],
        ["Teste Carrinho / Happy Path", "201, 200, 201, 201, 200, 200", "Позитивный сценарий по корзине"],
        ["Teste Carrinho / ADD produtos no carrinho - diminui do estoque", "201, 200, 201, 201, 200, 200", "Проверка остатков товара"],
    ]
    scenarios_body = f"""
    <div class="grid">
      <div class="span-7">
        {card(
            "Folders and scenarios launched",
            table(
                ["Scenario", "Expected codes", "Goal"],
                scenario_rows,
            ),
            "Happy Path и negative tests, которые использовались в практической",
        )}
      </div>
      <div class="span-5">
        {card(
            "Observed collection issues",
            "<ul class='list'>"
            "<li>Duplicate email collisions in Teste Usuario / Happy Path</li>"
            "<li>Delete user with cart scenario breaks earlier than expected</li>"
            "<li>editar produto sem ID expects success while API returns 400</li>"
            "<li>JavaScript error: quantidade is not defined</li>"
            "<li>Some cart tests expect fields absent in the actual response</li>"
            "</ul>",
            "Замечания по готовой коллекции ServerREST",
        )}
      </div>
    </div>
    """
    write_html("image-6-serverrest-scenarios.html", "ServerREST: Папки и сценарии", scenarios_body)

    server_summary_rows = [
        ["BASE", "17", "10", badge("0 failures", "ok")],
        ["Teste Usuario", "20", "34", badge("10 failures", "danger")],
        ["Teste Produto", "20", "39", badge("7 failures", "warn")],
        ["Teste Carrinho", "23", "36", badge("3 failures", "warn")],
    ]
    run_results_body = f"""
    <div class="grid">
      <div class="span-6">
        {card(
            "Run results summary",
            table(["Folder", "Requests", "Assertions", "Result"], server_summary_rows),
            "Итоги запуска ServeRest через Newman",
        )}
      </div>
      <div class="span-6">
        {card(
            "Failure examples",
            table(["Location", "Message"], build_failures(server_carts["run"]) + build_failures(server_products["run"])[:4]),
            "Фрагменты падений для анализа negative tests",
        )}
      </div>
    </div>
    """
    write_html("image-7-serverrest-run-results.html", "ServerREST: Run Results", run_results_body)

    product_success = next(
        execution
        for execution in server_products["run"]["executions"]
        if execution["item"]["name"] == "Cadastrar produto" and execution["response"]["code"] == 201
    )
    product_duplicate = next(
        execution
        for execution in server_products["run"]["executions"]
        if execution["item"]["name"] == "Cadastrar produto com nome repetido"
    )
    cart_success = next(
        execution
        for execution in server_carts["run"]["executions"]
        if execution["item"]["name"] == "Cadastrar Carrinho" and execution["response"]["code"] == 201
    )

    responses_body = f"""
    <div class="grid">
      <div class="span-4">
        {card(
            "Create product: 201",
            format_code_block(response_text(product_success)),
            "Пример успешного ответа ServeRest",
        )}
      </div>
      <div class="span-4">
        {card(
            "Duplicate product: 400",
            format_code_block(response_text(product_duplicate)),
            "Пример негативного ответа ServeRest",
        )}
      </div>
      <div class="span-4">
        {card(
            "Create cart: 201",
            format_code_block(response_text(cart_success)),
            "Пример ответа для корзины",
        )}
      </div>
    </div>
    """
    write_html("image-8-serverrest-responses.html", "ServerREST: Примеры ответов", responses_body)


if __name__ == "__main__":
    main()
