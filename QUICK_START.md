# 🚀 Quick Start - Analizador de Patrones

## 📥 Instalación (Una sola vez)

```bash
cd /root/projects/agentic-swarm
python3 -m venv venv
source venv/bin/activate
pip install scikit-learn pandas numpy scipy
```

## ⚡ Uso Rápido

### Opción 1: Ejecutar análisis completo
```bash
source venv/bin/activate
python example_usage.py
```

**Salida:**
- Resumen visual en terminal
- Archivo `analysis_results.json` con todos los detalles
- Recomendaciones accionables

### Opción 2: Usar en tu código Python
```python
from pattern_analyzer import MentalHealthPatternAnalyzer

# Crear analizador
analyzer = MentalHealthPatternAnalyzer('datasets/Teen_Mental_Health_Dataset.csv')

# Ejecutar análisis
results = analyzer.analyze_all_patterns()

# Ver resumen
analyzer.print_summary()

# Obtener insights
insights = analyzer.get_actionable_insights()
```

### Opción 3: Análisis específico
```python
# Solo correlaciones
correlations = results['correlation_analysis']

# Solo factores de riesgo
risk_factors = results['risk_factors']

# Solo clusters
clusters = results['clustering_patterns']

# Solo arquetipos
archetypes = results['behavioral_archetypes']
```

---

## 🎯 Principales Hallazgos

| Métrica | Valor |
|---------|-------|
| Tasa de depresión | 2.6% |
| Factor de riesgo #1 | Horas de sueño (20.7%) |
| Factor de riesgo #2 | Horas en redes sociales (18.9%) |
| Grupo más vulnerable | Alto SM + Alto estrés (12.5%) |

---

## 📊 6 Estrategias de Análisis

1. **Correlación** - Relaciones estadísticas lineales
2. **Risk Factors** - Predicción con Random Forest
3. **Clustering** - Agrupación K-means (4 clusters)
4. **Arquetipos** - Perfiles de riesgo específicos
5. **Anomalías** - Outliers estadísticos
6. **Perfiles** - Comparación deprimidos vs. normales

---

## 📁 Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `pattern_analyzer.py` | Clase principal MentalHealthPatternAnalyzer |
| `example_usage.py` | Ejemplo completo de uso |
| `README_PATTERN_ANALYZER.md` | Documentación técnica completa |
| `analysis_results.json` | Resultados en formato JSON |
| `datasets/Teen_Mental_Health_Dataset.csv` | Datos de entrada |

---

## 🔍 Arquetipos Identificados

### 1. High SM + High Stress 🔴
- **Riesgo:** 12.5% depresión
- **Tamaño:** 80 adolescentes
- **Intervención:** Reducir screen time y estrés

### 2. Sleep Deprived 🌙
- **Riesgo:** 7.5% depresión  
- **Tamaño:** 294 adolescentes
- **Intervención:** Mejorar higiene del sueño

### 3. Socially Isolated 😔
- **Riesgo:** 2.2% depresión
- **Tamaño:** 415 adolescentes
- **Intervención:** Aumentar interacción social

### 4. Low Activity ⚽
- **Riesgo:** 3.0% depresión
- **Tamaño:** 269 adolescentes
- **Intervención:** Fomentar actividad física

---

## 💾 Datos Guardados

Después de ejecutar `example_usage.py`, se genera:

```json
{
  "correlation_analysis": {...},
  "risk_factors": {...},
  "clustering_patterns": {...},
  "behavioral_archetypes": {...},
  "anomalies": {...},
  "depression_risk_profiles": {...}
}
```

📍 Ubicación: `analysis_results.json`

---

## 🛠️ Personalización

### Cambiar número de clusters
```python
# En _identify_clustering_patterns()
optimal_k = 5  # cambiar de 4 a 5
```

### Cambiar umbral de percentil para arquetipos
```python
# En _identify_behavioral_archetypes()
percentile = 0.70  # cambiar sensibilidad
```

### Cambiar features del Random Forest
```python
# En _identify_risk_factors()
rf = RandomForestClassifier(n_estimators=200, max_depth=15)
```

---

## 📞 Soporte

**Problema:** ModuleNotFoundError: No module named 'sklearn'

**Solución:**
```bash
source venv/bin/activate
pip install scikit-learn
```

---

## 📚 Más Información

Ver `README_PATTERN_ANALYZER.md` para:
- Explicación detallada de cada estrategia
- Interpretación de resultados
- Limitaciones del algoritmo
- Referencias técnicas

---

**Última actualización:** Abril 2026
