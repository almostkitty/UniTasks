## 1. Диаграмма вариантов использования (Use Case)

```
@startuml
left to right direction

actor "Пользователь" as User
actor "Администратор" as Admin

rectangle "Сервис аудита LLM" {

  User --> (Загрузить текст)
  User --> (Запустить анализ)
  User --> (Просмотреть результат)
  User --> (Просмотреть детальный отчёт)

  Admin --> (Управление параметрами анализа)
  Admin --> (Просмотр статистики)

  (Запустить анализ) ..> (Предобработка текста) : <<include>>
  (Запустить анализ) ..> (Вычисление метрик) : <<include>>
  (Запустить анализ) ..> (Расчёт вероятности LLM) : <<include>>

  (Просмотреть детальный отчёт) ..> (Просмотреть результат) : <<extend>>
}

@enduml
```


![Use Case](img/dPBDJi9G48NtVOe9Ard00nX2uXwNFW2X5PjWIKfDJ8m9FmiMaA1kNABn1GhQjF9JNc7k6tbc00F5H6K3fVVCD-SSRiEv32Xeak_MhmAoNT-f1MxJiwngBMZwbECnfpmtGuxnFUNGT3cItpcgjkYYvVZVmWV-u0KdlEJ4T4pNj5MSchPAp-nh5rJ1Lxrwmy70AqSGJKLEqFOmds0Y97d3g_szYXrHfNAUeplB8jrDXKAPJlWPn--c3K8….png)



## 2. Диаграмма классов (Class Diagram)

```
@startuml

class User {
  +id: int
  +email: string
  +password: string
}

class Document {
  +id: int
  +text: string
  +upload_date: datetime
}

class Metrics {
  +lexical_diversity: float
  +burstiness: float
  +entropy: float
  +avg_sentence_length: float
  +repetition_score: float
}

class AuditResult {
  +llm_probability: float
  +label: string
}

class Analyzer {
  +analyze(text): AuditResult
}

class Preprocessor {
  +clean(text): string
}

class MetricCalculator {
  +compute_metrics(text): Metrics
}

class ScoringModel {
  +predict(metrics): float
}

User --> Document
Document --> AuditResult
AuditResult --> Metrics

Analyzer --> Preprocessor
Analyzer --> MetricCalculator
Analyzer --> ScoringModel

@enduml
```


![Class Diagram](img/PLBBRiCW4BpxApWcgl83FbIAsckagbNE2CCsNMaD29OqQTL_ByGld5oGcTsPtHciISKeZX62-6s4U4BJ2hHSFg5NIAs87D2U2k1pwxSBPiR-caRV-AzEfnuiFsWmNBYMI9wSCj8eXbQKax67HUS0kLF7GORWWbgHD7Y6496lhVZCx9jkbq9aj11Z1UO5WlDrcpgVPCmmM0sIm9xugwe6y7a-exCoQXTWAithx9D1VeUOQ7H6r4iVNAS….png)


Код Python
``` python
class Metrics:
    def __init__(self, lexical_diversity, burstiness, entropy, avg_sentence_length, repetition_score):
        self.lexical_diversity = lexical_diversity
        self.burstiness = burstiness
        self.entropy = entropy
        self.avg_sentence_length = avg_sentence_length
        self.repetition_score = repetition_score


class AuditResult:
    def __init__(self, probability, label):
        self.llm_probability = probability
        self.label = label


class Preprocessor:
    def clean(self, text: str) -> str:
        return text.lower().strip()


class MetricCalculator:
    def compute_metrics(self, text: str) -> Metrics:
        # заглушка
        return Metrics(0.5, 3.0, 5.0, 10.0, 0.2)


class ScoringModel:
    def predict(self, metrics: Metrics) -> float:
        return 0.7


class Analyzer:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.calculator = MetricCalculator()
        self.model = ScoringModel()

    def analyze(self, text: str) -> AuditResult:
        clean_text = self.preprocessor.clean(text)
        metrics = self.calculator.compute_metrics(clean_text)
        probability = self.model.predict(metrics)

        label = "LLM" if probability > 0.5 else "Human"
        return AuditResult(probability, label)
```


## 3. Диаграмма последовательности (Sequence)

```
@startuml

actor User
participant "Frontend" as FE
participant "API" as API
participant "Analyzer" as Analyzer
participant "Metrics" as Metrics
participant "Model" as Model

User -> FE : Загружает текст
FE -> API : POST /audit
API -> Analyzer : analyze(text)

Analyzer -> Metrics : compute_metrics(text)
Metrics --> Analyzer : metrics

Analyzer -> Model : predict(metrics)
Model --> Analyzer : probability

Analyzer --> API : result
API --> FE : JSON
FE --> User : Отображение результата

@enduml
```


![Sequence](img/NP2nJiCm48PtFyMfKnagTWOa1Yg11ArKc97hUB2Knf5paIXJ2Iix6yzGX58G29xX_4QS7RSY6QASx__qwxzVAhGERYljH2aT6cLAMI2CfiuMg8ji1BA2wNbVF9jVn3t_1q8Xy_M3TfsQ7dtaIgCpgef4cWU0pNJUoM4I8eI3oIcdW1EW5zhIkz_u9zhnrFe6V4CjVVb7tmX66EHOJCvdYniubdLcK8HD458YLcKtZb7Vuv4G1uMfb8e….png)


## 4. Диаграмма состояний (State)

```
@startuml

[*] --> Загружен

Загружен --> Обрабатывается
Обрабатывается --> РассчитаныМетрики
РассчитаныМетрики --> РассчитанаВероятность
РассчитанаВероятность --> ГотовРезультат

ГотовРезультат --> [*]

@enduml
```


![State](img/ZP112i8m44NtSugk2xs25oczIn8NBYmKwiADI8_GAjMYf6Vu_qP-cvrWbI7CPFxxGoPbNcL5iSbmH8yh7RUuOKGq--max8o1JiA0de5xN5IFgZmRMnEJkvFW5JjC31AZeDE2E4nuOBBVo9T9EgqmXvcDEb7PorJR_sYQVD0rODRZEwrzr_fFrcyZWpvbHLtiPLxP2m00.png)


## 5. Диаграмма деятельности (Activity)

```
@startuml
start

:Загрузка текста пользователем;

:Предобработка текста;

:Вычисление метрик;

:Расчёт вероятности LLM;

if (Вероятность > 0.5?) then (да)
  :Классификация как LLM;
else (нет)
  :Классификация как Human;
endif

:Формирование отчёта;

:Отображение результата пользователю;

stop
@enduml
```


![Activity](/Users/herman/Documents/GitHub/UniTasks/sem8/spec-lang/img/ZL4nJiD04EpzYYr9WsXeWWGjHNX491mH2Gp2fhSDIWeY8j8WKG053xX0J2mdDb-O_H6p5v8294HnkZdjpEpkN9nqBQwZNcgE14SnIeDEFj7nnmRFSC-spfiGprgP43bCqPFnqyTI9tkeGfMPUNA4fKdlR13faEzrrpOhc2fqJ4zQjxcLKgdSq.png)