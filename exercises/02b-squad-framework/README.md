# Exercise 02B -- `/squad` 로 지속적인 팀 구성하기

> ⚠️ **토큰 비용 경고:** Squad도 `/fleet` 처럼 Exercise 02의 단일 에이전트 루프보다 AI 사용량이 많습니다. 여러 개의 명명된 에이전트를 실행할 수 있기 때문입니다. 이를 정당화할 실제 프로젝트가 없다면 이 실습은 읽기만 하고 실행은 건너뛰어도 좋습니다.

## 목표 (Goal)

오픈 소스 [Squad](https://github.com/bradygaster/squad) 프레임워크를 프로젝트에 설치하여, 이슈와 세션을 넘나들며 유지되는 명명된 에이전트(frontend, backend, tester, lead 등)로 구성된 지속적인 팀을 세팅합니다. Fleet의 일회용, 단일 목표 서브 에이전트와 대비됩니다.

## 사전 준비 (Pre-reqs)

- Exercise 02A를 완료했거나 최소한 읽어서 `/fleet` 과 `/squad` 의 차이를 이해하고 있어야 합니다.
- Node.js 22.5.0 이상, 그리고 npm.
- Git 설치 및 구성 완료.
- Squad의 Issues/PR 기능을 위해 [GitHub CLI (`gh`)](https://cli.github.com/) 설치.
- Copilot CLI 설치(Exercise 02A, Step 1 참고).
- Squad는 **알파(alpha) 소프트웨어** 이며, 릴리즈마다 CLI 명령이 변경될 수 있습니다.

## 설정 (Set Up)

### Step 1 -- 도구 확인

```bash
node --version
npm --version
git --version
gh --version
```

**✓ 검증:** 네 명령 모두 버전을 출력해야 합니다. Node.js는 22.5.0 이상이어야 합니다.

### Step 2 -- 프로젝트 생성(또는 선택)

먼저 스크래치 프로젝트에서 시도해도 되고, `starter-app` 클론에서 바로 실행해도 됩니다.

```bash
mkdir my-squad-demo && cd my-squad-demo
git init
```

**✓ 검증:** `git status` 를 실행하면 "No commits yet" 이 표시되어야 합니다.

### Step 3 -- Squad CLI 설치

```bash
npm install -g @bradygaster/squad-cli
squad init
```

Squad는 단계별로 세팅을 안내합니다. 미리 만들어진 팀으로 시작하려면:

```bash
squad init --preset default
```

이 명령은 완전한 구성의 squad(멤버, 헌장(charter), 라우팅 규칙 포함)를 즉시 스캐폴딩합니다.

**✓ 검증:** 프로젝트에 `.squad/team.md` 가 생성되었는지 확인합니다.

### Step 4 -- GitHub 인증

```bash
gh auth login
```

**✓ 검증:** `gh auth status` 를 실행하면 "Logged in to github.com" 이 표시되어야 합니다. 이는 Squad가 여러분을 대신해 Issue와 PR을 열 수 있게 해줍니다.

## 실습 과제 (Your Task)

### Step 1 -- Squad 에이전트로 Copilot 열기

```bash
copilot --agent squad --yolo
```

> `--yolo` 플래그는 툴 호출마다 승인 프롬프트를 건너뜁니다. Squad는 일반 세션에서 많은 툴 호출을 하므로, 이 플래그 없이는 계속 승인을 해야 합니다.

VS Code에서는 대신 Copilot Chat을 열고 에이전트 선택기에서 **Squad** 를 선택할 수 있습니다.

### Step 2 -- 무엇을 만들지 설명

채팅에서 Squad에게 프로젝트를 설명하세요:

```
I'm starting a new project. Set up the team.
Here's what I'm building: a CLI task manager in Python with Azure OpenAI tag suggestions.
```

### Step 3 -- 제안된 팀 확인

Squad는 작업에 적합한 명명된 전문가 팀(예: backend 에이전트, tester 에이전트, lead 에이전트)을 제안합니다. 제안을 검토하고 `yes` 로 확정합니다.

**✓ 검증:** Squad가 팀 준비 완료를 확인하고, `.squad/` 아래에 멤버들이 반영되어 있는지 확인합니다.

### Step 4 -- 팀에 작업 위임

Exercise 02에서 이슈를 Copilot에 할당했던 것처럼 Squad에게 실제 작업을 픽업하도록 요청하되, 이번엔 가장 적합한 전문가로 라우팅되도록 합니다:

```
Have the backend specialist add a --tag filter to the list command,
and have the tester write tests for it.
```

### Step 5 -- 지속성(persistence) 관찰

세션을 닫고 나중에 다시 열어보세요(`copilot --agent squad --yolo` 를 다시 실행하거나, VS Code에서 Squad를 다시 선택). 여러분의 팀, 컨텍스트, 이전 결정들이 `.squad/` 아래에 그대로 남아 있음을 확인하세요. 매번 처음부터 시작하는 Fleet 실행과 대비됩니다.

## 이후 Squad 업그레이드

```bash
npm install -g @bradygaster/squad-cli@latest
squad upgrade
```

`squad upgrade` 는 Squad가 소유한 파일과 워크플로우를 갱신하지만, 여러분의 `.squad/` 팀 상태는 절대 건드리지 않습니다. 따라서 에이전트, 결정, 히스토리는 그대로 보존됩니다.

## 확인사항

- 명명된 전문가에게 위임하는 것이 Exercise 02에서 이슈 전체를 하나의 Copilot 에이전트에 할당했던 것과 어떻게 달랐나요?
- Squad가 세션 간에 기억한 것 중, 새로 시작하는 `/fleet` 실행에서는 유지되지 않는 것은 무엇이었나요?
- `/squad` 를 `/fleet` 대신 선택할 때는 언제이며, 단일 Copilot 에이전트(Exercise 02)가 여전히 옳은 선택일 때는 언제인가요?

## 다음 단계 (Next Step)

[Chapter 2 - Assign to Copilot](../../docs/chapter-2-assign-to-copilot.md) 로 돌아가거나, [Chapter 3 - Review a Draft PR](../03-review-a-pr/README.md) 로 계속 진행하세요.
