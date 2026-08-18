# AI Genius Episode 1: Workshop


## "Code with AI: GitHub Copilot for AI-Native Coding Workflows"

환영합니다! 
이 Repo는 **AI Genius Episode 1** 실습 워크숍 Repo입니다. 
이슈 작성, Copilot에게 작업 위임, 생성된 코드 리뷰, 그리고 PR 코멘트를 통한 반복(iterate)까지 AI-Native 개발 루프 전 과정을 실습하게 됩니다.

---

## 학습 목표 (What You Will Learn)

- 개발자에게 "AI Native"란 실제로 무엇을 의미하는지
- Copilot이 필요로 하는 컨텍스트를 담은 이슈를 작성하는 방법
- Copilot에게 작업을 할당하고 동작을 관찰하는 방법
- Copilot이 생성한 PR을 시니어 개발자처럼 리뷰하는 방법
- 처음부터 다시 시작하지 않고 PR 코멘트로 반복(iterate)하는 방법
- 코딩 과정 전반에 걸쳐 AI와 협업하기 위한 모범 사례

---

## AI-Native 워크플로우 루프 (The AI-Native Workflow Loop)

```
IDEA
  └─► GitHub Issue  (describe the work)
        └─► Assign to Copilot  (Copilot agent picks it up)
              └─► Code is generated in a secure sandbox
                    └─► Draft PR is opened  (with session log)
                          └─► Human reviews and iterates via PR comments
                                └─► Merge and ship
```

이 워크플로우에서 당신은 **테크 리드(tech lead)** 입니다. Copilot은 *어떻게(how)* 를 처리하고, 당신은 *무엇을(what)* 그리고 *왜(why)* 를 정의합니다.

---

## 설정 안내 (Setup Instructions)

### 사전 준비 사항 (Prerequisites)

- GitHub Copilot에 접근 가능한 GitHub 계정
- [GitHub Copilot App](https://github.com/features/copilot) 설치 (데스크톱)
- 로컬에 Python 3.10+ 설치 (starter app 실행용)
- Git 설치

### 시작하기 (Get Started)

1. 이 저장소를 본인 GitHub 계정으로 **Fork** 하세요 (페이지 오른쪽 상단).

2. 포크한 저장소를 로컬에 **Clone** 하세요:
   ```bash
   git clone https://github.com/YOUR-USERNAME/AIGenius-GHCP-AINative.git
   cd AIGenius-GHCP-AINative
   ```

3. **Starter app 실행**:
   ```bash
   cd starter-app
   pip install -r requirements.txt
   python app.py add "Deploy the API" --priority high --due 2025-12-31 --tag work
   python app.py add "Buy coffee" --priority low --tag personal
   python app.py list
   python app.py stats
   ```

4. **GitHub Copilot App** 을 열고 포크한 저장소에 연결하세요.

5. [`exercises/01-write-an-issue`](./exercises/01-write-an-issue/README.md) 부터 시작하여 순서대로 실습을 진행하세요.

---
## 저장소 구조 (Repo Structure)

```
📁 AIGenius-GHCP-AINative/
  ├── README.md                        # Episode intro + setup instructions
  ├── .github/
  │   ├── copilot-instructions.md      # Copilot context: conventions, Azure patterns, secrets
  │   └── ISSUE_TEMPLATE/
  │       └── feature-request.md       # Issue template for AI-native workflow
  ├── exercises/
  │   ├── 01-write-an-issue/           # Task: write a well-formed issue (cloud/AI options)
  │   ├── 02-assign-to-copilot/        # Task: assign + observe
  │   ├── 02a-fleet-mode/              # Optional: parallel sub-tasks with /fleet
  │   ├── 02b-squad-framework/         # Optional: persistent agent team with /squad
  │   ├── 03-review-a-pr/              # Task: review and comment on a PR
  │   ├── 04-iterate/                  # Task: iterate via PR comments
  │   └── 05-azure-and-ai/             # Stretch: pre-written issues for Azure + OpenAI features
  └── starter-app/                     # Python CLI task manager to extend
      ├── app.py                       # CLI: add, list, complete, edit, delete, stats
      ├── requirements.txt             # click, rich, pytest
      └── tests/
          ├── conftest.py              # Shared fixtures (isolated task file)
          └── test_tasks.py            # 41 tests covering all commands + edge cases
```

---

## AI-Native 코딩의 5가지 황금률 (The 5 Golden Rules of AI-Native Coding)

1. **더 나은 이슈를 작성하라 (Write better issues)** -- 이슈가 곧 프롬프트입니다. 구체적으로 작성하세요.
2. **시니어 개발자처럼 리뷰하라 (Review like a senior dev)** -- AI는 빠르게 생성하고, 사람은 똑똑하게 검증합니다.
3. **`copilot-instructions.md` 를 활용하라 (Use `copilot-instructions.md`)** -- 프로젝트에 대한 상시 컨텍스트를 Copilot에게 제공하세요.
4. **처음부터 다시 만들지 말고 반복하라 (Iterate, don't regenerate)** -- 새로 시작하는 대신 코멘트로 방향을 안내하세요.
5. **루프 안에 머물러라 (Stay in the loop)** -- 세션 로그를 확인하고 Copilot이 무엇을 왜 했는지 이해하세요.


---

## 워크숍 문서 사이트 (Workshop Docs Site - MkDocs)

이 저장소에는 참가자용 MkDocs Material 문서 사이트가 포함되어 있습니다.

- 로컬에서 실행:
  ```bash
  pip install -r docs-requirements.txt
  mkdocs serve
  ```
- 로컬에서 빌드:
  ```bash
  mkdocs build --strict
  ```
- 배포(Deployments):
  - GitHub Actions 워크플로우 `.github/workflows/docs.yml` 은 `attendee-mkdocs-site` (그리고 `main`) 브랜치에 푸시가 발생할 때 사이트를 빌드하여 GitHub Pages에 배포합니다.
