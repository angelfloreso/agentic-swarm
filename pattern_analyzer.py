"""
Pattern Analyzer for Teen Mental Health Dataset
Identifies correlations, clustering patterns, and risk factors related to depression
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import pearsonr, spearmanr


class MentalHealthPatternAnalyzer:
    """
    Analyzes patterns in teen mental health data to identify risk factors
    and behavioral patterns related to depression.
    """
    
    def __init__(self, csv_path: str):
        """
        Initialize the analyzer with data from CSV file.
        
        Args:
            csv_path: Path to the dataset CSV file
        """
        self.df = pd.read_csv(csv_path)
        self.numerical_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        self.patterns = {}
        
    def analyze_all_patterns(self) -> Dict[str, Any]:
        """
        Execute all pattern analysis methods and return comprehensive results.
        
        Returns:
            Dictionary containing all identified patterns
        """
        results = {
            'correlation_analysis': self._analyze_correlations(),
            'risk_factors': self._identify_risk_factors(),
            'clustering_patterns': self._identify_clustering_patterns(),
            'behavioral_archetypes': self._identify_behavioral_archetypes(),
            'anomalies': self._identify_anomalies(),
            'depression_risk_profiles': self._analyze_depression_risk_profiles()
        }
        
        self.patterns = results
        return results
    
    def _analyze_correlations(self) -> Dict[str, Any]:
        """
        Analyze correlations between all numerical variables and depression label.
        
        Returns:
            Dictionary with correlation statistics
        """
        correlations = {}
        depression_col = 'depression_label'
        
        if depression_col not in self.df.columns:
            return {'error': 'depression_label not found'}
        
        for col in self.numerical_cols:
            if col != depression_col:
                pearson_corr, pearson_pval = pearsonr(self.df[col], self.df[depression_col])
                spearman_corr, spearman_pval = spearmanr(self.df[col], self.df[depression_col])
                
                correlations[col] = {
                    'pearson_correlation': round(pearson_corr, 4),
                    'pearson_pvalue': round(pearson_pval, 4),
                    'spearman_correlation': round(spearman_corr, 4),
                    'spearman_pvalue': round(spearman_pval, 4),
                    'strength': self._classify_correlation(pearson_corr)
                }
        
        # Sort by absolute correlation value
        sorted_corr = sorted(correlations.items(), 
                            key=lambda x: abs(x[1]['pearson_correlation']), 
                            reverse=True)
        
        return {
            'correlations': dict(sorted_corr),
            'strongest_predictors': [col for col, _ in sorted_corr[:5]]
        }
    
    def _identify_risk_factors(self) -> Dict[str, Any]:
        """
        Use Random Forest to identify feature importance for depression prediction.
        
        Returns:
            Dictionary with risk factor rankings
        """
        # Prepare data
        X = self.df[self.numerical_cols].drop('depression_label', axis=1)
        y = self.df['depression_label']
        
        # Train Random Forest
        rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        rf.fit(X, y)
        
        # Get feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': rf.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return {
            'feature_importance': feature_importance.to_dict('records'),
            'top_risk_factors': feature_importance.head(5)['feature'].tolist(),
            'model_accuracy': round(rf.score(X, y), 4)
        }
    
    def _identify_clustering_patterns(self) -> Dict[str, Any]:
        """
        Identify natural groupings in the data using K-means clustering.
        
        Returns:
            Dictionary with clustering insights
        """
        # Prepare and scale numerical data
        X = self.df[self.numerical_cols].drop('depression_label', axis=1)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Determine optimal clusters using elbow method
        inertias = []
        K_range = range(2, 8)
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
        
        # Use k=4 as optimal
        optimal_k = 4
        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Analyze each cluster
        self.df['cluster'] = clusters
        cluster_profiles = {}
        
        for cluster_id in range(optimal_k):
            cluster_data = self.df[self.df['cluster'] == cluster_id]
            
            cluster_profiles[f'cluster_{cluster_id}'] = {
                'size': len(cluster_data),
                'depression_rate': round(cluster_data['depression_label'].mean(), 4),
                'avg_stress': round(cluster_data['stress_level'].mean(), 2),
                'avg_anxiety': round(cluster_data['anxiety_level'].mean(), 2),
                'avg_social_media_hours': round(cluster_data['daily_social_media_hours'].mean(), 2),
                'avg_sleep_hours': round(cluster_data['sleep_hours'].mean(), 2),
                'avg_physical_activity': round(cluster_data['physical_activity'].mean(), 2)
            }
        
        return {
            'number_of_clusters': optimal_k,
            'cluster_profiles': cluster_profiles
        }
    
    def _identify_behavioral_archetypes(self) -> Dict[str, Any]:
        """
        Identify distinct behavioral archetypes based on key characteristics.
        
        Returns:
            Dictionary describing behavioral profiles
        """
        archetypes = {}
        
        # High Social Media, High Stress archetype
        high_sm_high_stress = self.df[
            (self.df['daily_social_media_hours'] > self.df['daily_social_media_hours'].quantile(0.75)) &
            (self.df['stress_level'] > self.df['stress_level'].quantile(0.75))
        ]
        archetypes['high_sm_high_stress'] = {
            'count': len(high_sm_high_stress),
            'depression_rate': round(high_sm_high_stress['depression_label'].mean(), 4),
            'avg_anxiety': round(high_sm_high_stress['anxiety_level'].mean(), 2),
            'avg_addiction': round(high_sm_high_stress['addiction_level'].mean(), 2),
            'description': 'High social media usage with elevated stress levels'
        }
        
        # Sleep Deprived archetype
        sleep_deprived = self.df[self.df['sleep_hours'] < self.df['sleep_hours'].quantile(0.25)]
        archetypes['sleep_deprived'] = {
            'count': len(sleep_deprived),
            'depression_rate': round(sleep_deprived['depression_label'].mean(), 4),
            'avg_stress': round(sleep_deprived['stress_level'].mean(), 2),
            'avg_anxiety': round(sleep_deprived['anxiety_level'].mean(), 2),
            'avg_screen_before_sleep': round(sleep_deprived['screen_time_before_sleep'].mean(), 2),
            'description': 'Insufficient sleep patterns'
        }
        
        # Socially Isolated archetype
        isolated = self.df[self.df['social_interaction_level'] == 'low']
        archetypes['socially_isolated'] = {
            'count': len(isolated),
            'depression_rate': round(isolated['depression_label'].mean(), 4),
            'avg_stress': round(isolated['stress_level'].mean(), 2),
            'avg_anxiety': round(isolated['anxiety_level'].mean(), 2),
            'avg_physical_activity': round(isolated['physical_activity'].mean(), 2),
            'description': 'Low social interaction levels'
        }
        
        # Low Activity archetype
        low_activity = self.df[self.df['physical_activity'] < self.df['physical_activity'].quantile(0.25)]
        archetypes['low_activity'] = {
            'count': len(low_activity),
            'depression_rate': round(low_activity['depression_label'].mean(), 4),
            'avg_stress': round(low_activity['stress_level'].mean(), 2),
            'avg_social_media_hours': round(low_activity['daily_social_media_hours'].mean(), 2),
            'description': 'Minimal physical activity'
        }
        
        return archetypes
    
    def _identify_anomalies(self) -> Dict[str, Any]:
        """
        Identify statistical outliers and unusual patterns.
        
        Returns:
            Dictionary with anomaly information
        """
        anomalies = {}
        
        # Z-score based anomaly detection
        from scipy import stats
        
        z_scores = np.abs(stats.zscore(self.df[self.numerical_cols]))
        anomaly_mask = (z_scores > 2.5).any(axis=1)
        anomalies['statistical_outliers'] = {
            'count': int(anomaly_mask.sum()),
            'percentage': round(anomaly_mask.sum() / len(self.df) * 100, 2),
            'depression_rate_in_outliers': round(self.df[anomaly_mask]['depression_label'].mean(), 4)
        }
        
        # Contradictory patterns (high stress but good academic performance)
        contradictory = self.df[
            (self.df['stress_level'] > 7) & 
            (self.df['academic_performance'] > 3.5)
        ]
        anomalies['contradictory_patterns'] = {
            'high_stress_good_grades': len(contradictory),
            'depression_rate': round(contradictory['depression_label'].mean(), 4)
        }
        
        return anomalies
    
    def _analyze_depression_risk_profiles(self) -> Dict[str, Any]:
        """
        Analyze specific risk profiles for depression cases.
        
        Returns:
            Dictionary with depression-specific patterns
        """
        depressed = self.df[self.df['depression_label'] == 1]
        non_depressed = self.df[self.df['depression_label'] == 0]
        
        profiles = {}
        
        for col in self.numerical_cols:
            if col != 'depression_label':
                profiles[col] = {
                    'depressed_avg': round(depressed[col].mean(), 2),
                    'non_depressed_avg': round(non_depressed[col].mean(), 2),
                    'difference': round(depressed[col].mean() - non_depressed[col].mean(), 2),
                    'depressed_std': round(depressed[col].std(), 2),
                    'non_depressed_std': round(non_depressed[col].std(), 2)
                }
        
        return {
            'depression_rate': round(depressed.shape[0] / len(self.df), 4),
            'risk_profiles': profiles,
            'sample_size': {
                'depressed': len(depressed),
                'non_depressed': len(non_depressed)
            }
        }
    
    @staticmethod
    def _classify_correlation(correlation: float) -> str:
        """Classify correlation strength."""
        abs_corr = abs(correlation)
        if abs_corr >= 0.7:
            return 'Very Strong'
        elif abs_corr >= 0.5:
            return 'Strong'
        elif abs_corr >= 0.3:
            return 'Moderate'
        elif abs_corr >= 0.1:
            return 'Weak'
        else:
            return 'Very Weak'
    
    def get_actionable_insights(self) -> List[str]:
        """
        Generate actionable insights from identified patterns.
        
        Returns:
            List of actionable recommendations
        """
        if not self.patterns:
            self.analyze_all_patterns()
        
        insights = []
        
        # Insight from risk factors
        top_factors = self.patterns['risk_factors']['top_risk_factors']
        insights.append(f"Priority intervention areas: {', '.join(top_factors)}")
        
        # Insight from archetypes
        highest_risk_archetype = max(
            self.patterns['behavioral_archetypes'].items(),
            key=lambda x: x[1]['depression_rate']
        )
        insights.append(f"Highest risk group: {highest_risk_archetype[0]} with "
                       f"{highest_risk_archetype[1]['depression_rate']*100:.1f}% depression rate")
        
        # Insight from anomalies
        outlier_depression = self.patterns['anomalies']['statistical_outliers']['depression_rate_in_outliers']
        insights.append(f"Outlier individuals show {outlier_depression*100:.1f}% depression rate")
        
        return insights
    
    def print_summary(self) -> None:
        """Print a formatted summary of all analysis."""
        if not self.patterns:
            self.analyze_all_patterns()
        
        print("\n" + "="*70)
        print("TEEN MENTAL HEALTH PATTERN ANALYSIS SUMMARY")
        print("="*70)
        
        print("\n📊 CORRELATION ANALYSIS")
        print("-" * 70)
        for factor, data in list(self.patterns['correlation_analysis']['correlations'].items())[:5]:
            print(f"  {factor}: {data['pearson_correlation']} ({data['strength']})")
        
        print("\n⚠️  RISK FACTORS")
        print("-" * 70)
        for item in self.patterns['risk_factors']['feature_importance'][:5]:
            print(f"  {item['feature']}: {item['importance']:.4f}")
        
        print("\n👥 BEHAVIORAL ARCHETYPES")
        print("-" * 70)
        for archetype, data in self.patterns['behavioral_archetypes'].items():
            depression_pct = data['depression_rate'] * 100
            print(f"  {archetype} (n={data['count']}): {depression_pct:.1f}% depression rate")
        
        print("\n💡 ACTIONABLE INSIGHTS")
        print("-" * 70)
        for insight in self.get_actionable_insights():
            print(f"  • {insight}")
        
        print("\n" + "="*70 + "\n")


def main():
    """Main execution function."""
    # Initialize analyzer
    analyzer = MentalHealthPatternAnalyzer('datasets/Teen_Mental_Health_Dataset.csv')
    
    # Run all analyses
    results = analyzer.analyze_all_patterns()
    
    # Print summary
    analyzer.print_summary()
    
    return analyzer, results


if __name__ == "__main__":
    analyzer, results = main()
