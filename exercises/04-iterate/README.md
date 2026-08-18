# Exercise 04 -- PR 코멘트로 반복(Iterate)하기

## 목표 (Goal)

처음부터 다시 시작하는 대신, PR 코멘트를 통해 Copilot의 결과물을 다듬어 갑니다.

## 사고 모델 (The Mental Model)

Copilot을 아주 빠르고, 매우 직역적이며, 명확한 지시가 필요한 주니어 개발자로 생각해보세요. 여러분은 그의 작업을 버리고 스스로 다시 쓰는 것이 아니라, 피드백을 주어 개선하도록 하는 것입니다.

이것이 협업적 반복(collaborative iteration) 입니다. 처음부터 다시 하지 않고, 다듬어 갑니다.

---

## 실습 과제 (Your Task)

### Step 1 -- Exercise 03에서 남긴 코멘트 확인

Exercise 03에서 리뷰했던 드래프트 PR로 돌아가, 변경을 요청했던 코멘트를 찾습니다.

### Step 2 -- Copilot의 반응 관찰

Copilot이 여러분의 코멘트를 픽업해 브랜치를 업데이트합니다. 관찰해보세요:

- 피드백을 어떻게 해석하는지
- 요청된 변경을 어떻게 반영하는지
- 같은 PR에 업데이트된 코드를 어떻게 푸시하는지

### Step 3 -- 재리뷰

Copilot의 응답이 반영되면 업데이트된 diff를 리뷰합니다:

- 피드백이 올바르게 반영되었는가?
- 새로운 이슈가 생기지는 않았는가?
- 이제 머지할 준비가 되었는가?

### Step 4 -- 추가 피드백(선택)

추가 개선이 필요하면 코멘트를 하나 더 남기세요. 이번에는 훨씬 더 구체적으로.

효과적인 반복 코멘트의 예:

> "The validation you added rejects empty strings, but it does not trim whitespace first. A task name of '   ' (spaces only) should also be rejected."

> "Can you move the CSV export logic into its own function? The current implementation mixes I/O and formatting in a way that will be hard to test."

> "The error message on line 42 says 'invalid input' but doesn't tell the user what valid input looks like. Can you improve it?"

### Step 5 -- 승인 및 머지

PR에 만족했다면:

1. PR을 **Draft** 에서 **Ready for Review** 로 변경합니다.
2. 최종 리뷰 승인을 남깁니다.
3. PR을 머지합니다.

기억하세요: **Copilot은 머지할 수 없습니다.** 최종 관문은 언제나 사람입니다. 이것은 의도된 설계입니다. AI-Native는 AI 자율(AI-autonomous)이 아니라 AI 협업(AI-collaborative)을 의미합니다.

---

## 회고 질문 (Reflection Questions)

- 만족스러운 결과에 도달하기까지 몇 번의 반복이 필요했나요?
- 코멘트의 정밀도가 Copilot 업데이트의 품질에 어떤 영향을 미쳤나요?
- 반복 횟수를 줄이기 위해 원래 이슈에서 무엇을 다르게 했을까요?

---

## 축하합니다 (Congratulations)

여러분은 AI-Native 개발의 전체 루프를 완성했습니다:

```
Write Issue  ─►  Assign to Copilot  ─►  Review PR  ─►  Iterate  ─►  Merge
```

여러분은 테크 리드(tech lead)로서 무엇을, 왜 만들지 정의했습니다. Copilot은 구현을 맡았습니다. 여러분은 결과를 검증하고 완성까지 이끌었습니다.

그것이 바로 AI-Native 개발입니다.

---

## 다음은? (What Next?)

- [GitHub Copilot documentation](https://docs.github.com/en/copilot) 살펴보기
- [Copilot CLI](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line) 사용해보기: `gh copilot suggest "undo my last commit but keep the changes"`
- 여러분의 프로젝트 중 하나에 `copilot-instructions.md` 를 작성해보기
