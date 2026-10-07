import { getClassifierResults } from "@/lib/api";
import { FeatureRadarChart } from "@/components/charts/FeatureRadarChart";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export const dynamic = "force-dynamic";


export default async function FeaturesPage() {
  const results = await getClassifierResults();
  
  // Aggregate features by true label
  const featureAggregates: Record<string, Record<string, { sum: number, count: number }>> = {
    non_autistic: {},
    autistic_tier_1: {},
    autistic_tier_2: {},
    autistic_tier_3: {},
  };

  const featureNames = new Set<string>();

  results.forEach(result => {
    const tier = result.trueLabel;
    Object.entries(result.features).forEach(([feature, val]) => {
      featureNames.add(feature);
      if (!featureAggregates[tier][feature]) {
        featureAggregates[tier][feature] = { sum: 0, count: 0 };
      }
      featureAggregates[tier][feature].sum += val;
      featureAggregates[tier][feature].count += 1;
    });
  });

  // Prepare data for Recharts
  const chartData = Array.from(featureNames).map(feature => {
    const formatName = feature.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    return {
      subject: formatName,
      non_autistic: featureAggregates["non_autistic"][feature] ? featureAggregates["non_autistic"][feature].sum / featureAggregates["non_autistic"][feature].count : 0,
      autistic_tier_1: featureAggregates["autistic_tier_1"][feature] ? featureAggregates["autistic_tier_1"][feature].sum / featureAggregates["autistic_tier_1"][feature].count : 0,
      autistic_tier_2: featureAggregates["autistic_tier_2"][feature] ? featureAggregates["autistic_tier_2"][feature].sum / featureAggregates["autistic_tier_2"][feature].count : 0,
      autistic_tier_3: featureAggregates["autistic_tier_3"][feature] ? featureAggregates["autistic_tier_3"][feature].sum / featureAggregates["autistic_tier_3"][feature].count : 0,
    };
  });

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Behavioral Features</h1>
        <p className="text-muted-foreground">
          Divergence of extracted linguistic and behavioral features across severity tiers.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Feature Radar</CardTitle>
          <CardDescription>
            Click the badges below to toggle specific severity tiers.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FeatureRadarChart data={chartData} />
        </CardContent>
      </Card>
    </div>
  );
}
