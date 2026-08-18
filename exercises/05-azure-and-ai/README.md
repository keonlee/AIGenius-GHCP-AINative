# Exercise 05 -- Azure + AI: 클라우드 네이티브 확장

## 목표 (Goal)

Copilot이 실제 클라우드 SDK 연동과 AI 기능 개발을 어떻게 처리하는지 살펴보고, 왜 이런 작업이 인상적이면서도 위임 시 위험할 수 있는지 이해합니다.

## 왜 다른가 (Why This Is Different)

이전 실습에서는 Copilot이 로컬 Python 앱을 확장했습니다. 이번에는 Copilot이 다음을 수행해야 하는 이슈를 작성합니다:

- 클라우드 저장을 위해 **Azure SDK** (`azure-data-tables`) 사용
- 런타임 AI 동작을 위해 **Azure OpenAI** 호출
- 환경 변수로 비밀 값(secret)을 안전하게 처리
- 클라우드 호출을 mock한 테스트 작성

이는 복잡도가 크게 상승하는 지점입니다. 이슈의 품질과 리뷰 스킬이 가장 중요해지는 지점이기도 합니다.

---

## Option 1: 저장소를 Azure Table Storage로 마이그레이션

### 아키텍처 (The Architecture)

```
CLI (app.py)
    └─► storage.py  (new abstraction layer)
            ├─► LocalStorage (current JSON file — default)
            └─► AzureTableStorage (new — activated by env var)
```

`AZURE_STORAGE_CONNECTION_STRING` 이 설정되면 앱은 Azure Table Storage를 사용하고, 그렇지 않으면 기존 로컬 JSON 파일로 폴백(fallback)합니다. **호환성이 깨지는 변경은 없습니다.**

### 미리 작성된 이슈 (Pre-Written Issue)

이 내용을 Exercise 01 이슈(Option A)로 사용하거나, 새 이슈를 만들어 아래 내용을 넣으세요:

---

**Title:** Migrate task storage to Azure Table Storage

**Problem statement:**
Tasks are currently stored in a local JSON file (`tasks.json`). This means data is lost when the machine changes and cannot be shared across devices. We need a cloud-backed storage option.

**Desired behaviour:**
- When the `AZURE_STORAGE_CONNECTION_STRING` environment variable is set, tasks are stored in and retrieved from an Azure Table Storage table named `tasks`.
- When the environment variable is not set, the app falls back to the existing local JSON file behaviour.
- All existing CLI commands (`add`, `list`, `complete`, `edit`, `delete`, `stats`) work identically regardless of which storage backend is active.

**Acceptance criteria:**
- [ ] A new `storage.py` module defines a `TaskStorage` protocol with `load() -> list[dict]` and `save(tasks: list[dict]) -> None` methods
- [ ] `LocalStorage` implements `TaskStorage` using the existing JSON file approach
- [ ] `AzureTableStorage` implements `TaskStorage` using `azure-data-tables`
- [ ] `app.py` calls `get_storage()` to obtain the correct implementation at startup
- [ ] `AZURE_STORAGE_CONNECTION_STRING` is loaded from a `.env` file using `python-dotenv` if present
- [ ] If the env var is set but the connection fails, the app prints a clear error and exits with code 1
- [ ] `azure-data-tables` and `python-dotenv` are added to `requirements.txt`
- [ ] Tests cover both storage implementations (mock Azure calls with `unittest.mock`)
- [ ] No connection strings or account keys appear in source code

**Constraints:**
- Use `azure-data-tables` (not the older `azure-storage-table` SDK)
- Use `PartitionKey = "tasks"` and `RowKey = str(task["id"])` for Azure entities
- Do not change the CLI interface or task schema

**Definition of Done:**
- [ ] `python app.py add "Test" && python app.py list` works with a real Azure Storage account
- [ ] All existing tests still pass
- [ ] New tests cover `AzureTableStorage` with mocked Azure calls

---

### PR에서 확인할 사항 (What to Look for in the PR)

Copilot의 구현을 리뷰할 때 특히 다음에 주목하세요:

- **자격 증명을 하드코딩하지 않았는가?** 그렇다면 심각한 보안 문제입니다.
- **저장소 추상화가 실제로 두 구현을 분리하는가?** 아니면 모든 것을 `app.py` 에 인라인했는가?
- **Azure 에러가 우아하게(graceful) 처리되는가?** 아니면 원시 Python 스택 트레이스를 그대로 뱉는가?
- **테스트가 실제로 격리되어 있는가?** Azure 호출은 반드시 mock되어야 하며, 실제 호출이 아니어야 합니다.

---

## Option 2: Azure OpenAI 태스크 카테고리 분류 추가

### 아키텍처 (The Architecture)

```
python app.py add "Renew SSL certificate"
    └─► Azure OpenAI: "Suggest a category for: Renew SSL certificate"
            └─► returns: "devops"
                    └─► task saved with tags: ["devops"]
```

### 미리 작성된 이슈 (Pre-Written Issue)

---

**Title:** Add Azure OpenAI smart tag suggestion to `add` command

**Problem statement:**
Users often forget to tag tasks when adding them. We want to use Azure OpenAI to suggest a single category tag automatically when no tags are provided.

**Desired behaviour:**
- When `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, and `AZURE_OPENAI_DEPLOYMENT` are all set AND the user does not provide any `--tag` arguments, call Azure OpenAI to suggest a single tag for the task.
- The suggested tag is added automatically and displayed to the user: `[AI suggested tag: devops]`
- If any of the env vars are missing, or if the AI call fails, the task is saved without a tag (graceful degradation — never block the user).
- Add a `--no-ai` flag to `add` that skips the AI suggestion entirely.

**Acceptance criteria:**
- [ ] `suggest_tag(task_name: str, description: str) -> str | None` function in a new `ai.py` module
- [ ] Uses `openai.AzureOpenAI` with credentials from environment variables
- [ ] System prompt instructs the model to return a single lowercase tag (no punctuation)
- [ ] `add` command calls `suggest_tag` only when no `--tag` flags are provided and `--no-ai` is not set
- [ ] Graceful degradation: any exception from the AI call is caught and logged, task is saved normally
- [ ] `openai` added to `requirements.txt`
- [ ] Tests for `suggest_tag` mock the OpenAI client — no real API calls in tests

**Constraints:**
- The AI call must not block the user for more than 5 seconds (use `timeout=5` in the client)
- Never log or print the raw API key
- The `--no-ai` flag is documented in `--help`

**Definition of Done:**
- [ ] `python app.py add "Deploy to production"` with env vars set shows an AI-suggested tag
- [ ] `python app.py add "Deploy" --no-ai` skips the AI call
- [ ] All existing tests still pass
- [ ] New tests cover `suggest_tag` with mocked responses and error cases

---

### PR에서 확인할 사항 (What to Look for in the PR)

- **AI 호출이 정말로 선택적인가?** 환경 변수가 설정되지 않아도 앱이 동작해야 합니다.
- **타임아웃이 강제되는가?** 느린 OpenAI 호출이 CLI를 블록해서는 안 됩니다.
- **프롬프트가 잘 설계되었는가?** Copilot에게 시스템 프롬프트를 보여달라고 요청하세요. 출력 형식을 명확히 제약하고 있나요?
- **에러가 조용히 삼켜지지는 않는가?** 에러는 잡히고 로깅되어야 하며, 조용히 무시되어서는 안 됩니다.

---

## 스트레치 골 (Stretch Goal): 전체 루프를 두 번 실행하기

1. AI-Native 루프를 통해 Copilot과 함께 Option 1(Azure storage)을 완료
2. 머지 후, Option 2(Azure OpenAI)에 대한 새 이슈를 작성하여 루프를 다시 실행

끝나면 다음을 갖춘 앱이 완성됩니다:
- Azure Table Storage에 태스크 저장
- 생성 시 AI로 태스크 자동 카테고리 분류
- mock된 클라우드 호출을 갖춘 전체 테스트 스위트
- 모든 자격 증명은 환경 변수에서 로드

이것이 여러분과 Copilot의 협업으로 만들어진, 프로덕션 수준의 AI-Native 클라우드 애플리케이션입니다.

---

## 다음 단계 (Next Steps)

- [Azure Table Storage Python quickstart](https://learn.microsoft.com/en-us/azure/storage/tables/table-storage-quickstart-create-python) 읽기
- [Azure OpenAI Python quickstart](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?pivots=programming-language-python) 읽기
- [GitHub Copilot documentation](https://docs.github.com/en/copilot) 살펴보기
