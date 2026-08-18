# Exercise 02A -- `/fleet` 으로 병렬 실행하기

> ⚠️ **토큰 비용 경고:** `/fleet` 은 하나가 아니라 여러 서브 에이전트(subagent)를 띄웁니다. 개인 유료 플랜을 사용 중이며 이를 정당화할 실제 백로그가 없다면, 이 실습은 읽어보기만 하고 실제 실행은 건너뛰어도 좋습니다.

## 목표 (Goal)

Copilot CLI의 `/fleet` 슬래시 명령을 사용하여 하나의 목표를 독립적인 서브 태스크들로 분할하고, 서브 에이전트가 병렬로 처리하도록 만듭니다. Exercise 02에서 진행한 단일 이슈 루프를 하나씩 순차 실행하는 것과 대비됩니다.

## 사전 준비 (Pre-reqs)

- Exercise 02(이슈 할당과 샌드박스 루프 관찰)를 완료했습니다.
- Node.js 22+ 가 설치되어 있습니다(Copilot CLI 요구 사항).
- `starter-app` 클론에 접근 가능한 터미널.
- 사용 중인 플랜에서 [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli) 접근 권한.

## 설정 (Set Up)

### Step 1 -- Copilot CLI 설치

사용 중인 OS에 맞는 방법을 선택하세요:

```bash
# npm (모든 OS, Node.js 22+ 필요)
npm install -g @github/copilot

# Homebrew (macOS/Linux)
brew install --cask copilot-cli

# WinGet (Windows)
winget install GitHub.Copilot

# 설치 스크립트 (macOS/Linux)
curl -fsSL https://gh.io/copilot-install | bash
```

**✓ 검증:** `copilot --version` 을 실행하여 버전 번호가 출력되는지 확인합니다.

### Step 2 -- 인증

```bash
copilot
```

처음 실행할 때는 대화형 프롬프트를 따라 GitHub 계정으로 로그인합니다.

**✓ 검증:** `copilot` 을 다시 실행하면 로그인 요청 없이 바로 세션으로 진입해야 합니다.

## 실습 과제 (Your Task)

### Step 1 -- 저장소에서 세션 열기

`starter-app` 클론의 루트에서:

```bash
copilot
```

### Step 2 -- 독립적 서브 태스크가 있는 목표를 `/fleet` 에 전달

대화형 세션 안에서 실행:

```
/fleet Break the remaining Exercise 05 work into independent sub-tasks
(Azure OpenAI client setup, tag suggestion function, tests) and
work them in parallel
```

또는 쉘에서 비대화형으로 실행(대화형 모드 외부에서는 `--no-ask-user` 플래그가 필요):

```bash
copilot -p "/fleet Break the remaining Exercise 05 work into independent sub-tasks (Azure OpenAI client setup, tag suggestion function, tests) and work them in parallel" --no-ask-user
```

### Step 3 -- 오케스트레이터가 작업하는 것을 관찰

Copilot의 메인 에이전트는 다음을 수행합니다:

1. 목표를 분석하고 독립적인 서브 태스크로 분할 가능한지 판단합니다.
2. 오케스트레이터로서 병렬 실행이 가능한 서브 에이전트에게 서브 태스크를 배정합니다.
3. 각 서브 에이전트는 같은 파일 시스템을 공유하면서 자체 컨텍스트 윈도우에서 작업합니다.
4. 오케스트레이터가 결과를 모아 하나의 통합 결과로 재조립합니다.

### Step 4 -- 통합 결과 리뷰

`/fleet` 이 끝나면 단일 에이전트 PR과 마찬가지로 결과를 리뷰하세요. diff를 확인하고, 테스트가 실행되었는지 확인하며, 순차적으로 처리되어야 할 것이 잘못 병렬화되지는 않았는지(예: 다른 서브 태스크의 산출물에 의존하는 태스크) 확인합니다.

## 좋은 `/fleet` 프롬프트를 위한 팁

- 산출물(deliverables)을 명확히 밝히세요. 예: 각 워커가 소유해야 할 파일이나 모듈을 정확히 나열.
- 분할이 자명하도록 프롬프트를 구조화하세요(예: "Create `docs/authentication.md`, `docs/endpoints.md`, `docs/errors.md`").
- 모호한 프롬프트는 병렬 대신 순차적으로 처리될 수 있습니다. `/fleet` 은 독립성을 증명할 수 있는 작업만 병렬화합니다.
- 순차적 작업(step 2가 step 1의 구체적 산출물을 필요로 함)이나 워커들이 같은 파일을 두고 경합할 만큼 강하게 결합된 편집에는 `/fleet` 을 피하세요.

## 회고 질문 (Reflection Questions)

- Copilot이 목표를 실제로 병렬 서브 태스크로 분할했나요, 아니면 순차 실행했나요? 그 이유는?
- `/fleet` 결과를 리뷰하는 것이 Exercise 02의 단일 에이전트 PR 리뷰와 어떻게 달랐나요?
- 여러분의 백로그에서 `/fleet` 에 잘 맞는 작업은 어떤 종류이고, 그렇지 않은 작업은 어떤 종류인가요?

## 다음 단계 (Next Step)

[Exercise 02B - Persistent Teams with `/squad`](../02b-squad-framework/README.md) 로 계속 진행하세요.
