# Exercise 03 -- 드래프트(Draft) PR 리뷰하기

## 목표 (Goal)

Copilot이 만든 pull request를 시니어 개발자의 비판적인 시선으로 리뷰합니다.

## 가장 중요한 스킬 (Your Most Important Skill)

AI-Native 워크플로우에서 **비판적 리뷰(critical review)** 는 가장 가치 있는 활동입니다. Copilot은 그럴듯한(plausible) 코드를 만들어내는 데 매우 능합니다. 그러나 그럴듯한 것이 곧 올바르거나(correct), 안전하거나(secure), 여러분의 실제 의도에 부합하는(aligned) 것을 의미하지는 않습니다.

여러분은 품질의 관문입니다. AI는 빠르게 생성하고, 여러분은 똑똑하게 검증합니다.

---

## 실습 과제 (Your Task)

### Step 1 -- 드래프트 PR 열기

1. 저장소의 **Pull Requests** 탭으로 이동합니다.
2. Copilot이 이슈로부터 생성한 드래프트 PR을 엽니다.

### Step 2 -- 세션 로그 읽기

코드 diff를 보기 전에, Copilot이 PR 설명에 포함한 세션 로그를 먼저 읽어보세요. 여기에는 다음이 설명되어 있습니다:

- 이슈를 어떻게 해석했는지
- 어떤 결정을 왜 내렸는지
- 무엇을 하지 않기로 선택했는지

### Step 3 -- Diff 리뷰

**Files changed** 탭에서 변경 사항을 꼼꼼히 검토합니다. 아래 체크리스트를 리뷰 가이드로 사용하세요.

---

## PR 리뷰 체크리스트 (PR Review Checklist)

Copilot이 생성한 모든 PR에 이 체크리스트를 사용하세요:

**정확성 (Correctness)**
- [ ] 코드가 이슈의 수용 기준(acceptance criteria)에 부합하는가?
- [ ] 엣지 케이스가 처리되는가?(빈 입력, 잘못된 값, 누락된 데이터)
- [ ] 로직이 처음부터 끝까지 이치에 맞는가?

**코드 품질 (Code Quality)**
- [ ] 코드가 읽기 쉽고 나머지 코드베이스와 일관성이 있는가?
- [ ] 함수가 작고 초점이 명확한가?
- [ ] 새 함수에 타입 힌트(type hints)와 docstring이 있는가?

**보안 (Security)**
- [ ] 하드코딩된 자격 증명, API 키, 비밀 값이 없는가
- [ ] 사용자 입력이 사용 전에 검증되는가
- [ ] 명백한 injection 또는 파싱 취약점이 없는가

**의존성 (Dependencies)**
- [ ] 새로운 의존성이 정당하고 `requirements.txt` 에 선언되었는가?
- [ ] 임포트된 라이브러리가 실제로 사용되고 있는가?

**테스트 (Tests)**
- [ ] 기존 테스트가 여전히 통과하는가?
- [ ] 새 동작에 대한 새 테스트가 있는가?

---

## 실습 과제 (계속)

4. 위 체크리스트를 따라 리뷰를 진행합니다.
5. PR에 변경을 요청하거나 명확화(clarifying) 질문을 하는 **코멘트를 최소 1개 이상** 남깁니다.

좋은 코멘트는 구체적입니다. 예를 들어 다음과 같이 쓰지 말고:
> "This could be better"

이렇게 시도해보세요:
> "Can you add input validation to the task name field? It should reject empty strings and names longer than 200 characters."

---

## 회고 질문 (Reflection Questions)

- Copilot이 수용 기준에서 놓친 부분이 있었나요?
- 세션 로그의 결정 중 동의하기 어려운 것이 있었나요?
- 상세한 이슈를 작성한 것이 PR 품질에 어떤 영향을 미쳤나요?

---

## 다음 단계 (Next Step)

리뷰 코멘트를 남긴 뒤에는 [Exercise 04 -- Iterate via PR Comments](../04-iterate/README.md) 로 이동하세요.
