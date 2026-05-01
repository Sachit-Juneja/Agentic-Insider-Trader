import { FinalReport } from "@/lib/types";
import { Card } from "@/components/ui/card";

export function FundamentalHealth({ report }: { report: FinalReport }) {
  const agentData = report?.agent_breakdown?.find(a => a.name.includes("Fundamental"));
  
  if (!agentData) return <div className="text-slate-500">No fundamental data available.</div>;

  return (
    <div className="space-y-6">
      <Card className="bg-[#0d1333] border-slate-800 p-6">
        <h4 className="text-[#00d4ff] font-bold uppercase mb-4 border-b border-slate-800 pb-2">Fundamental Verdict</h4>
        <p className="text-slate-300 font-sans leading-relaxed text-sm mb-4">
          {agentData.summary}
        </p>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 uppercase font-bold">Signal:</span>
          <span className={`text-xs font-bold px-2 py-1 rounded ${agentData.signal === 'bullish' ? 'bg-[#00ff88]/20 text-[#00ff88]' : agentData.signal === 'bearish' ? 'bg-[#ff3366]/20 text-[#ff3366]' : 'bg-slate-700 text-slate-300'}`}>
            {agentData.signal.toUpperCase()}
          </span>
          <span className="text-xs text-slate-500 ml-4 uppercase font-bold">Score:</span>
          <span className="text-xs font-bold text-slate-200">{agentData.score.toFixed(1)}/100</span>
        </div>
      </Card>

      <div>
        <h4 className="text-[#00d4ff] font-bold uppercase mb-3 border-b border-slate-800 pb-2">Key Findings</h4>
        <div className="space-y-2">
          {agentData.key_findings?.map((finding: string, i: number) => (
            <div key={i} className="flex items-start gap-2 p-2 bg-[#0a0e27] border border-slate-800/50 rounded">
              <div className="mt-1 w-1.5 h-1.5 rounded-full bg-[#00d4ff] shrink-0" />
              <p className="text-sm text-slate-300">{finding}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
