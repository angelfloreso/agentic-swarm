# Teen Mental Health Pattern Analyzer

## 📋 Descripción General

Este algoritmo identifica patrones significativos en datos de salud mental de adolescentes, enfocándose en detectar factores de riesgo relacionados con la depresión. Utiliza múltiples técnicas de análisis de datos para proporcionar una visión integral del comportamiento y bienestar mental de los adolescentes.

---

## 🎯 Estrategia de Análisis

El algoritmo emplea **6 estrategias complementarias** para identificar patrones:

### 1. **Análisis de Correlación** (`_analyze_correlations`)
**Objetivo:** Identificar relaciones lineales entre variables individuales y la depresión.

**Técnica:**
- Correlación de Pearson: para relaciones lineales
- Correlación de Spearman: para relaciones monotónicas (más robusta)
- Cálculo de p-valores para validar significancia estadística
- Clasificación de fortaleza: Very Weak → Very Strong

**Ventajas:**
- Identifica rápidamente predictores individuales
- Proporciona métricas estadísticas confiables
- Ordena automáticamente por relevancia

**Ejemplo de uso:**
```python
# Identifica que "anxiety_level" tiene correlación fuerte con depresión
# mientras que "physical_activity" tiene correlación inversa
```

---

### 2. **Identificación de Factores de Riesgo** (`_identify_risk_factors`)
**Objetivo:** Determinar qué características predicen mejor la depresión.

**Técnica:**
- **Random Forest Classifier**: 100 árboles de decisión
- Feature Importance (importancia de características): mide cuánto contribuye cada variable a las predicciones
- Máxima profundidad de 10 para evitar sobreajuste

**Ventajas:**
- Captura relaciones no-lineales y complejas
- Menos sensible a valores atípicos
- Identifica interacciones entre variables
- Proporciona puntuación de precisión del modelo

**Resultado:** Lista ordenada de factores de riesgo principales

---

### 3. **Patrones de Agrupamiento** (`_identify_clustering_patterns`)
**Objetivo:** Encontrar grupos naturales de adolescentes con perfiles similares.

**Técnica:**
- **K-means Clustering**: agrupa observaciones en K grupos
- **StandardScaler**: normaliza datos antes de clustering
- **Elbow Method**: determina número óptimo de clusters (k=4)
- **PCA** (preparado para análisis dimensional)

**Proceso:**
1. Normaliza todas las variables numéricas
2. Prueba 2-7 clusters
3. Identifica 4 clusters como óptimo
4. Perfila cada cluster por indicadores de salud mental

**Información por Cluster:**
- Tamaño del grupo
- Tasa de depresión
- Niveles promedio de estrés, ansiedad, actividad física
- Patrones de sueño y uso de redes sociales

---

### 4. **Arquetipos de Comportamiento** (`_identify_behavioral_archetypes`)
**Objetivo:** Crear perfiles de riesgo específicos basados en umbral de percentiles.

**Arquetipos Identificados:**

| Arquetipo | Criterios | Indicador Clave |
|-----------|-----------|-----------------|
| **High SM + High Stress** | Social media >75º percentil + Estrés >75º percentil | Adicción y ansiedad |
| **Sleep Deprived** | Sueño <25º percentil | Pantalla antes de dormir, estrés |
| **Socially Isolated** | Interacción social = "low" | Patrón de depresión |
| **Low Activity** | Actividad física <25º percentil | Comportamiento sedentario |

**Ventaja:** Identifica grupos de alto riesgo específicos para intervención dirigida

---

### 5. **Detección de Anomalías** (`_identify_anomalies`)
**Objetivo:** Identificar casos inusuales que requieren atención especial.

**Técnicas:**

**A) Análisis Z-score:**
- Detecta valores > 2.5 desviaciones estándar
- Identifica outliers estadísticos
- Calcula tasa de depresión en outliers

**B) Patrones Contradictorios:**
- Alto estrés pero buen desempeño académico
- Puede indicar afrontamiento positivo o enmascaramiento de síntomas

---

### 6. **Perfiles de Riesgo de Depresión** (`_analyze_depression_risk_profiles`)
**Objetivo:** Comparar características entre adolescentes con y sin depresión.

**Análisis:**
- Promedio de cada variable por estado de depresión
- Diferencia entre grupos
- Desviación estándar para entender variabilidad
- Tasa general de depresión en la población

**Útil para:** Identificar qué variables cambian más dramáticamente en casos de depresión

---

## 🔧 Uso

### Instalación de dependencias
```bash
pip install pandas numpy scikit-learn scipy
```

### Uso básico
```python
from pattern_analyzer import MentalHealthPatternAnalyzer

# Inicializar
analyzer = MentalHealthPatternAnalyzer('datasets/Teen_Mental_Health_Dataset.csv')

# Ejecutar análisis completo
results = analyzer.analyze_all_patterns()

# Obtener resumen
analyzer.print_summary()

# Obtener insights accionables
insights = analyzer.get_actionable_insights()
for insight in insights:
    print(f"• {insight}")
```

### Acceso a resultados específicos
```python
# Correlaciones
correlations = results['correlation_analysis']

# Factores de riesgo
risk_factors = results['risk_factors']

# Clusters
clusters = results['clustering_patterns']

# Arquetipos
archetypes = results['behavioral_archetypes']
```

---

## 📊 Salida del Análisis

### Estructura de resultados:
```python
{
    'correlation_analysis': {
        'correlations': {...},
        'strongest_predictors': [...]
    },
    'risk_factors': {
        'feature_importance': [...],
        'top_risk_factors': [...],
        'model_accuracy': 0.XX
    },
    'clustering_patterns': {
        'number_of_clusters': 4,
        'cluster_profiles': {...}
    },
    'behavioral_archetypes': {...},
    'anomalies': {...},
    'depression_risk_profiles': {...}
}
```

---

## 💡 Ventajas del Enfoque Multi-Estrategia

| Estrategia | Detecta | Fortaleza |
|-----------|---------|----------|
| Correlación | Relaciones lineales | Rápido, interpretable |
| Risk Factors | Predictores complejos | Captura interacciones |
| Clustering | Subpoblaciones | Segmentación de intervenciones |
| Arquetipos | Riesgos específicos | Perfiles actionables |
| Anomalías | Casos inusuales | Intervención personalizada |
| Perfiles Riesgo | Diferencias de grupo | Contexto clínico |

---

## 🎯 Casos de Uso

1. **Identificación de adolescentes en riesgo:** Detecta perfiles de alto riesgo para derivación
2. **Planificación de intervenciones:** Diferentes estrategias por arquetipo
3. **Predicción de depresión:** Usa Random Forest para pronóstico
4. **Investigación:** Valida hipótesis sobre factores de salud mental
5. **Monitoreo longitudinal:** Sigue cambios en patrones a lo largo del tiempo

---

## ⚙️ Parámetros Configurables

```python
# En MentalHealthPatternAnalyzer:

# K-means clusters
optimal_k = 4  # Cambiar según necesidad

# Umbral Z-score para anomalías
z_threshold = 2.5  # Aumentar para menos outliers

# Random Forest
n_estimators = 100  # Más = mejor pero más lento
max_depth = 10  # Limitar profundidad para evitar sobreajuste

# Percentiles para arquetipos
percentile_threshold = 0.75  # Ajustar sensibilidad
```

---

## 📈 Interpretación de Resultados

### Correlación fuerte (>0.7 o <-0.7)
- Relación significativa con depresión
- Considerar como objetivo de intervención

### Importancia de característica >0.15
- Factor significativo según modelo
- Priorizar en intervenciones

### Tasa de depresión por cluster
- Cluster X% > promedio = alto riesgo
- Cluster X% < promedio = factor protector

### Anomalías >3% de población
- Grupo no negligible requiere atención
- Posible subpoblación no captada por arquetipos

---

## 🔍 Limitaciones

1. **Correlación ≠ Causalidad:** La correlación no implica que una variable cause depresión
2. **Dependencia de datos:** La calidad del análisis depende de la calidad y representatividad de los datos
3. **Sesgos de clasificación:** `depression_label` puede no capturar todos los casos
4. **Factores no medidos:** Pueden existir variables importantes no presentes en el dataset

---

## 📚 Referencias Técnicas

- **Scikit-learn:** https://scikit-learn.org/
- **Pearson vs Spearman:** https://en.wikipedia.org/wiki/Correlation
- **K-means Clustering:** https://en.wikipedia.org/wiki/K-means_clustering
- **Random Forest:** https://en.wikipedia.org/wiki/Random_forest
- **Z-score Anomaly Detection:** https://en.wikipedia.org/wiki/Standard_score

---

## 👨‍💻 Autor
Algoritmo de análisis de patrones para salud mental de adolescentes - 2026

## 📄 Licencia
MIT

---

**Última actualización:** Abril 2026
