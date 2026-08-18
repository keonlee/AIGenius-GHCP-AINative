# Exercise 02 -- Copilot에게 이슈 할당하기

## 목표 (Goal)

작성한 이슈를 Copilot에게 위임하고 실시간으로 작업 과정을 관찰합니다. 기다리는 동안 Copilot Chat과 Copilot CLI를 사용해 코드베이스를 탐색합니다.

## 마인드셋의 전환 (The Mindset Shift)

과거 워크플로우에서는 이슈를 작성한 뒤 IDE를 열고 직접 코딩을 시작했습니다. AI-Native 워크플로우에서는 이 작업을 팀원에게 방금 위임한 것과 같습니다. 이제 여러분의 역할은 **가이드하고 리뷰하는 것(guide and review)** 이며, 모든 코드 라인을 직접 타이핑하는 것이 아닙니다.

Copilot은 이 작업을 수행하기 위해 안전하고 격리된 GitHub Actions VM을 띄웁니다. 프로덕션 환경을 건드릴 수 없고, 승인 없이 머지할 수 없으며, 전체 세션 로그를 남기므로 무엇을 왜 했는지 정확히 확인할 수 있습니다.

---

## 실습 과제 (Your Task)

### Step 1 -- 이슈 할당

1. Exercise 01에서 작성한 이슈를 엽니다.
2. 오른쪽 **Assignees** 패널에서 톱니바퀴 아이콘을 클릭합니다.
3. 목록에서 **Copilot** 을 검색해 선택합니다.
4. 할당을 저장합니다.

Assignee 목록에 Copilot이 표시되고, 이슈에 작업을 픽업했다는 코멘트가 나타나야 합니다.

### Step 2 -- Copilot App 열기

1. 데스크톱에서 **GitHub Copilot App** 을 엽니다.
2. **My Work** 뷰로 이동합니다.
3. 여러분의 이슈에 대한 활성 세션을 찾습니다.

### Step 3 -- 관찰

Copilot이 작업하는 모습을 지켜봅니다. 다음을 볼 수 있습니다:

- 저장소를 안전한 샌드박스에 클론
- 기존 구조를 이해하기 위해 코드베이스 탐색
- 코드 변경 수행
- 결정 사항을 설명하는 세션 로그와 함께 드래프트(draft) PR 오픈

아직은 개입하지 말고, 그저 관찰만 하세요.

### Step 4 -- Copilot Chat으로 탐색

에이전트 세션이 백그라운드에서 돌아가는 동안, 로컬에 클론한 `starter-app` 을 대상으로 편집기(VS Code, JetBrains 또는 github.com 채팅 패널)에서 **Copilot Chat** 을 엽니다. 다음을 물어보세요:

- `@workspace explain how app.py stores and loads tasks`
- `@workspace what would I need to change to add a new field to a task?`
- `app.py` 의 `list` 명령에 대해 `/explain`

이는 Copilot과 다른 방식으로 협업하는 모드입니다. 전체 작업을 위임하는 대신 대화를 통해 이해를 쌓아가는 것이지요. Chat의 답변이 실제 워크스페이스의 파일들, 즉 지금 에이전트가 샌드박스에서 편집하고 있는 바로 그 코드베이스에 근거해 이루어진다는 점에 주목하세요.

### Step 5 -- Copilot CLI로 탐색

[GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli) 가 설치되어 있다면 저장소 루트의 터미널에서 시도해보세요:

```bash
gh copilot suggest "run the starter-app tests and show a summary of failures"
gh copilot explain "python app.py stats"
```

---

## 더 깊이 (Go Deeper - Optional): 하나의 이슈에서 플릿(fleet)으로 확장

> ⚠️ **토큰 비용 경고:** 아래 두 실습은 방금 실행한 "1 이슈 - 1 에이전트" 루프보다 AI 사용량이 더 큽니다. `/fleet` 과 `/squad` 는 하나가 아니라 **여러** 에이전트 세션을 띄웁니다. 개인 유료 플랜을 사용 중이며 이를 정당화할 실제 프로젝트가 없다면, 링크된 실습을 읽어보기만 하고 실제 실행은 건너뛰어도 좋습니다.

지금까지 여러분은 AI-Native 작업의 가장 작은 단위인 "1 이슈, 1 에이전트, 1 PR" 을 수행했습니다. 이는 시작하기에 적절한 지점이지만, 열 개의 이슈가 동시에 진행되는 실제 스프린트로 확장되지는 않습니다. 여기서 `/fleet` 과 `/squad` 가 등장합니다. 두 가지 모두 같은 질문에 대한 다른 답변입니다: *한 명의 개발자가 한 에이전트를 지시하는 방식에서, 팀 전체가 다수의 에이전트를 동시에 지시하는 방식으로 어떻게 넘어가는가?*

### `/fleet`: 병렬, 상태 비저장(stateless) 실행

`/fleet` 은 병렬, 상태 비저장 실행을 위해 만들어진 Copilot CLI 명령입니다. 하나의 목표(objective)를 주면 오케스트레이터(orchestrator) 에이전트가 그것을 독립적인 서브 태스크들로 쪼개고, 어떤 것이 blocking 없이 실행 가능한지 확인한 다음 병렬로 실행합니다.

이렇게 생각해보세요: 오늘날 단일 Copilot 에이전트가 이슈 하나를 픽업하는 개발자 한 명이라면, `/fleet` 은 관련된 이슈 열 개를 한 번에 할당하고 열 명의 단명(short-lived) 계약자가 동시에 처리한 뒤 결과를 합쳐서 돌려주는 것과 같습니다.

**단계별로 해보기:** [Exercise 02A - Parallel Execution with `/fleet`](../02a-fleet-mode/README.md) 는 Copilot CLI 설치, 인증, 직접 `/fleet` 프롬프트를 실행하는 과정을 안내합니다.

### `/squad`: 지속(persistent)되는 에이전트 팀

`/squad` 는 다른 형태의 해법입니다. 단일 CLI 명령이 아니라, 저장소에 설치하여 이름을 가진(named) 에이전트로 구성된 지속적인 팀을 만들어주는 오픈 소스 프레임워크입니다. Fleet의 일회용 서브 에이전트와 달리, Squad의 에이전트는 이슈와 세션을 넘나들며 계속 남아 있습니다.

Fleet이 단일 스프린트를 위한 계약자라면, Squad는 팀에 상주 전문가(permanent specialists)를 고용하는 것에 더 가깝습니다. 이들은 시간이 지나며 컨텍스트를 쌓아가고, 대량의 병렬 처리량이 필요할 때는 내부적으로 Fleet을 사용할 수도 있습니다.

**단계별로 해보기:** [Exercise 02B - A Persistent Team with `/squad`](../02b-squad-framework/README.md) 는 Squad CLI 설치, 팀 초기화, 명명된 전문가에게 작업을 위임하는 과정을 안내합니다.

### 이것이 클라우드 네이티브 아키텍처와 어떻게 매핑되는가

- **`/fleet` 은 인지 작업(cognitive work)의 수평 확장(horizontal scaling)입니다.** 클라우드 네이티브 앱이 로드 밸런서 뒤에서 상태 비저장 컴퓨트 인스턴스를 확장하여 부하를 흡수하듯이, `/fleet` 은 상태 비저장 서브 에이전트를 확장하여 백로그를 흡수합니다.
- **`/squad` 는 지속적 상태를 가진 오래 살아있는 서비스 메시(service mesh)에 더 가깝습니다.** 일시적인 파드(pod) 대신, 자체 메모리와 책임을 가진 특화되고 주소 지정 가능한(addressable) 에이전트들이 서로 협업합니다.
- **`/fleet` 내부의 웨이브(wave) 기반 의존성 스케줄링** — 실행 가능한 것을 먼저 실행하고, 대기하고, 다음 웨이브를 실행하는 방식 — 은 CI/CD 파이프라인이나 Kubernetes 잡 그래프에서 이미 알고 있는 DAG 스케줄링과 개념적으로 동일합니다.

핵심 요점: 이 실습의 단일 이슈 루프는 "hello world" 입니다. `/fleet` 과 `/squad` 는 같은 루프를 여러분이 매 에이전트 세션마다 개인적으로 감독하지 않고도 실제 팀의 백로그 규모로 확장하는 방법입니다.

### 안전 모델은 그대로 유지됩니다

`/fleet` 도 `/squad` 도 핵심 안전 모델을 바꾸지 않습니다. 일회용(Fleet)이든 지속적(Squad)이든 모든 서브 에이전트는 여전히 PR을 열고, 자기 작업을 스스로 머지할 수 없으며, 프로덕션 접근이 없는 격리된 샌드박스에서 실행됩니다. 모두 이 실습 Step 1에서 본 것과 동일한 GitHub 컨트롤 플레인의 지배를 받습니다. 에이전트가 늘어난다는 것은 리뷰가 줄어드는 것이 아니라, 리뷰할 병렬 제안이 늘어난다는 뜻입니다.
