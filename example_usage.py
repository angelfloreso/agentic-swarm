"""
Ejemplo de uso simplificado del Pattern Analyzer
Demuestra cómo usar el analizador de patrones
"""

from pattern_analyzer import MentalHealthPatternAnalyzer
import json


def main():
    """Ejemplo completo de uso del analizador."""
    
    # 1. Inicializar el analizador
    print("🔄 Inicializando analizador...")
    analyzer = MentalHealthPatternAnalyzer('datasets/Teen_Mental_Health_Dataset.csv')
    
    # 2. Ejecutar análisis completo
    print("📊 Ejecutando análisis de patrones...")
    results = analyzer.analyze_all_patterns()
    
    # 3. Mostrar resumen
    print("\n")
    analyzer.print_summary()
    
    # 4. Obtener insights accionables
    print("\n🎯 RECOMENDACIONES ACCIONABLES")
    print("="*70)
    insights = analyzer.get_actionable_insights()
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    
    # 5. Analizar grupos específicos
    print("\n\n👥 ANÁLISIS DETALLADO POR ARQUETIPO")
    print("="*70)
    archetypes = results['behavioral_archetypes']
    
    for archetype_name, data in archetypes.items():
        depression_pct = data['depression_rate'] * 100
        print(f"\n📍 {archetype_name.upper().replace('_', ' ')}")
        print(f"   Tamaño del grupo: {data['count']} adolescentes")
        print(f"   Tasa de depresión: {depression_pct:.1f}%")
        
        # Mostrar características principales
        if 'avg_stress' in data:
            print(f"   Estrés promedio: {data['avg_stress']}/10")
        if 'avg_anxiety' in data:
            print(f"   Ansiedad promedio: {data['avg_anxiety']}/10")
        if 'avg_social_media_hours' in data:
            print(f"   Horas en redes: {data['avg_social_media_hours']} hrs/día")
        if 'avg_sleep_hours' in data:
            print(f"   Horas de sueño: {data['avg_sleep_hours']} hrs/noche")
    
    # 6. Mostrar factores de riesgo principales
    print("\n\n⚠️  FACTORES DE RIESGO PRINCIPALES")
    print("="*70)
    risk_data = results['risk_factors']
    
    print(f"\nPrecisión del modelo: {risk_data['model_accuracy']*100:.1f}%")
    print("\nTop 5 factores de riesgo:")
    for i, factor_data in enumerate(risk_data['feature_importance'][:5], 1):
        importance = factor_data['importance'] * 100
        print(f"   {i}. {factor_data['feature']}: {importance:.1f}%")
    
    # 7. Guardar resultados en JSON
    print("\n\n💾 GUARDANDO RESULTADOS...")
    print("="*70)
    
    # Convertir resultados a JSON (algunas conversiones necesarias)
    json_safe_results = convert_results_to_json_safe(results)
    
    with open('analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(json_safe_results, f, indent=2, ensure_ascii=False)
    
    print("✅ Resultados guardados en: analysis_results.json")
    
    # 8. Estadísticas de la población
    print("\n\n📈 ESTADÍSTICAS DE LA POBLACIÓN")
    print("="*70)
    depression_stats = results['depression_risk_profiles']
    
    print(f"Tasa general de depresión: {depression_stats['depression_rate']*100:.1f}%")
    print(f"Adolescentes con depresión: {depression_stats['sample_size']['depressed']}")
    print(f"Adolescentes sin depresión: {depression_stats['sample_size']['non_depressed']}")


def convert_results_to_json_safe(results):
    """
    Convierte los resultados a formato JSON seguro.
    """
    def convert_value(val):
        if isinstance(val, (int, float, str, bool, type(None))):
            return val
        elif isinstance(val, dict):
            return {k: convert_value(v) for k, v in val.items()}
        elif isinstance(val, (list, tuple)):
            return [convert_value(item) for item in val]
        else:
            return str(val)
    
    return convert_value(results)


if __name__ == "__main__":
    main()
