# WORKFLOW: TEST → BUG → CODE → RETEST
## Proces automat pentru funcționalități lipsă

---

## 🔄 FLOW COMPLET

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   TESTER    │────▶│   TEST      │────▶│   PASS?     │
│   START     │     │  EXECUTION  │     │             │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                           ┌────────────────────┘
                           │ YES
                           ▼
                    ┌─────────────┐
                    │    ✅ PASS  │
                    │   Mark DONE │
                    └─────────────┘
                           │
                           │ NO
                           ▼
                    ┌─────────────┐
                    │   ❌ FAIL   │
                    │  De ce?     │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │BUG în    │    │Funcțional│    │Eroare    │
    │cod       │    │itatea nu │    │de test   │
    │existent  │    │există    │    │(date)    │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
         ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │Assign la │    │Creez TASK│    │Tester    │
    │builder-1 │    │pentru    │    │fixează   │
    │(bug fix) │    │coder     │    │datele    │
    └──────────┘    └──────────┘    └──────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   CODER     │
                    │ IMPLEMENT   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  CODE REVIEW│
                    │   (QA)      │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   MERGE     │
                    │   to DEV    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  RETEST     │
                    │  (același   │
                    │   tester)   │
                    └─────────────┘
```

---

## 📋 REGULI PENTRU TESTERI

### Când un test FAIL:

#### 1. Analizează DE CE a eșuat:
```
□ Verifică dacă elementul există în HTML (DOM)
□ Verifică dacă API endpoint răspunde
□ Verifică dacă JavaScript funcționează (console errors)
□ Verifică dacă datele există în DB
```

#### 2. Categorizează problema:

| Tip | Descriere | Acțiune |
|-----|-----------|---------|
| **BUG** | Cod existent dar nu funcționează corect | Assign la builder-1 |
| **MISSING** | Funcționalitatea nu există deloc | Creez TASK pentru coder |
| **TEST ERROR** | Date de test greșite sau configurație | Tester fixează |

---

## 🎯 EXEMPLU: Container 8 - Setup-uri Incomplete

### Test Case TC8.1: Afișare Setup-uri Incomplete
```
Precondiții: Robotul V31 a găsit un setup dar nu a deschis tranzacție
Pași:
1. Accesează dashboard
2. Navighează la "Setup-uri Incomplete"
```

### Scenarii posibile:

#### ✅ SCENARIUL A: Totul funcționează
- Containerul există în HTML ✅
- Endpoint `/api/incomplete_setups` există și răspunde ✅
- Datele se afișează corect ✅
- **REZULTAT:** PASS → Mark as DONE

#### ❌ SCENARIUL B: Endpoint-ul nu există
- Containerul există în HTML ✅
- Endpoint `/api/incomplete_setups` returnează 404 ❌
- **ANALIZĂ:** Funcționalitatea nu există în backend
- **ACȚIUNE:** Creez TASK pentru coder

#### ❌ SCENARIUL C: Containerul nu există
- Containerul NU există în HTML ❌
- **ANALIZĂ:** UI nu este implementat
- **ACȚIUNE:** Creez TASK pentru coder (frontend)

---

## 📝 TEMPLATE TASK PENTRU CODER

### Task Type: IMPLEMENTATION_REQUIRED

```markdown
# TASK: Implementare [Nume Funcționalitate]
## Container: [X. Nume Container]

### Status: 🔴 BLOCKED - Testare imposibilă

### Ce lipsește:
- [ ] Endpoint API: [detalii]
- [ ] UI Component: [detalii]
- [ ] JavaScript Logic: [detalii]
- [ ] Database Schema: [detalii]

### Specificații (din documentație):
[Q8.1=A] Setup găsit dar nu s-a deschis tranzacție
[Q8.2=D] Timp configurabil în listă
[Q8.3=B+C+D] Acțiuni: Forțare + Ignorare + Modificare
[Q8.4=D] Toate informațiile afișate

### API Endpoint necesar:
```
GET /api/incomplete_setups
Response: {
  "status": "success",
  "setups": [...]
}
```

### UI necesar:
- Tabel cu coloane: Simbol, Direcție, Scor, Motiv, Preț, SL, TP, R:R, Timestamp, Robot
- Butoane: "Forțare Trade", "Ignoră", "Modifică"
- Configurare timp expirare

### Prioritate: P1 (HIGH)
### Estimated: 4 ore
### Assigned to: builder-1
```

---

## 🤖 WORKFLOW AUTOMAT

### Hook: test_completed
```python
# Pseudo-code pentru automatizare
def on_test_completed(test_result):
    if test_result.status == "FAIL":
        if test_result.reason == "MISSING_FUNCTIONALITY":
            # Creează task automat
            task = create_task(
                type="IMPLEMENTATION_REQUIRED",
                container=test_result.container,
                specifications=get_specifications(test_result.container),
                assign_to="builder-1",
                priority="P1"
            )
            # Notifică coder
            notify_coder(task)
            # Update taskboard
            update_taskboard(status="BLOCKED", task_id=task.id)
        elif test_result.reason == "BUG":
            # Creează bug report
            bug = create_bug_report(
                severity="HIGH",
                component=test_result.container,
                steps_to_reproduce=test_result.steps,
                expected=test_result.expected,
                actual=test_result.actual
            )
            assign_bug(bug, "builder-1")
```

---

## 📊 TRACKING STATUS

### Board Columns:
| Column | Descriere |
|--------|-----------|
| 📋 TO TEST | Teste gata de execuție |
| 🔄 TESTING | În execuție |
| ✅ PASSED | Test trecut |
| ❌ FAILED | Test eșuat - analiză în curs |
| 🔴 BLOCKED | Necesită implementare (task creat) |
| 🛠️ IN DEV | Coder lucrează la implementare |
| 👀 CODE REVIEW | Așteaptă review |
| 🔄 READY TO RETEST | Gata pentru retestare |

---

## 🎯 REGULI DE AUR

### Pentru Tester:
1. **NICIODATĂ** nu marca un test ca "FAIL" fără să verifici DE CE
2. **DOCUMENTEAZĂ** exact ce lipsește (API, UI, date)
3. **CREAZĂ TASK** clar și detaliat pentru coder
4. **FOLLOW-UP** când task-ul e marcat "DONE"

### Pentru Coder:
1. **CITEȘTE** specificațiile din documentație
2. **IMPLEMENTEAZĂ** conform răspunsurilor utilizatorului
3. **TESTEAZĂ LOCAL** înainte de commit
4. **UPDATE** task-ul cu ce ai făcut

### Pentru QA-Master:
1. **REVIEW** toate task-urile create
2. **VERIFICĂ** că specificațiile sunt clare
3. **PRIORITIZEAZĂ** corect (P0/P1/P2)
4. **MONITORIZEAZĂ** progresul

---

## ✅ CHECKLIST PENTRU FIECARE CONTAINER

### Înainte să începi testarea:
- [ ] Citit specificațiile din TEST_SPECIFICATION.md
- [ ] Verificat dacă containerul există în HTML
- [ ] Verificat dacă API-urile răspund
- [ ] Pregătit date de test

### După ce testul eșuează:
- [ ] Documentat exact ce lipsește
- [ ] Categorizat: BUG / MISSING / TEST_ERROR
- [ ] Creat task/bug report detaliat
- [ ] Notificat echipa relevantă

### După implementare:
- [ ] Retestat aceleași pași
- [ ] Verificat că toate cazurile sunt acoperite
- [ ] Marcat testul ca PASS/DONE

---

## 🚀 PORNIRE TESTARE

**Testerii încep cu:**
1. Container 1: Clienți (Q1.1-A, Q1.2-A+C, etc.)
2. Container 2: Poziții (Q2.1-C, Q2.2-B, etc.)
3. Container 5: V31 Robot (Q5.1-A+B, Q5.3-A, etc.)

**Dacă găsesc funcționalități lipsă:**
→ Creează task automat cu specificațiile din documentație

**Echipa de coderi primește task-uri și implementează.**

**Totul track-uit în TASKBOARD.json**

---

**Ești de acord cu acest workflow? Vrei să ajustez ceva?** 🚀
