import { FinalReport } from "@/lib/types";
import { Card } from "@/components/ui/card";

export function FlowAnalysis({ report }: { report: FinalReport }) {
  const data = report?.flow_analysis;
  if (!data) return <div className="text-slate-500">No flow data available.</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <Card className="bg-[#0a0e27] border-slate-800 p-4">
          <h4 className="text-xs text-slate-500 font-bold uppercase mb-2">Put/Call Ratio</h4>
          <p className="text-xl font-black text-slate-200">{data.put_call_ratio?.toFixed(2)}</p>
        </Card>
        <Card className="bg-[#0a0e27] border-slate-800 p-4">
          <h4 className="text-xs text-slate-500 font-bold uppercase mb-2">Dark Pool Volume</h4>
          <p className="text-xl font-black text-slate-200">{data.dark_pool_pct}%</p>
        </Card>
      </div>

      <div>
        <h4 className="text-[#00d4ff] font-bold uppercase mb-3 border-b border-slate-800 pb-2">Institutional Bias</h4>
        <Card className="bg-[#0d1333] border-slate-800 p-6 flex flex-col items-center justify-center">
          <p className={`text-2xl font-black uppercase ${data.institutional_bias === 'accumulation' ? 'text-[#00ff88]' : data.institutional_bias === 'distribution' ? 'text-[#ff3366]' : 'text-slate-400'}`}>
            {data.institutional_bias || 'Neutral'}
          </p>
          <p className="text-xs text-slate-500 mt-2 text-center">Based on block trade side estimates and dark pool positioning</p>
        </Card>
      </div>

      <div>
        <h4 className="text-[#00d4ff] font-bold uppercase mb-3 border-b border-slate-800 pb-2">Unusual Options Activity</h4>
        <div className="space-y-2">
          {data.unusual_trades?.map((t: any, i: number) => (
            <div key={i} className="flex justify-between items-center p-3 bg-[#0d1333] border border-slate-800 rounded">
              <div className="flex items-center gap-3">
                <span className={`px-2 py-1 text-[10px] font-bold rounded ${t.type === 'CALL' ? 'bg-[#00ff88]/20 text-[#00ff88]' : 'bg-[#ff3366]/20 text-[#ff3366]'}`}>
                  {t.type} {t.size}
                </span>
                <div>
                  <p className="text-sm font-bold text-slate-200">{t.dte} Days to Expiry</p>
                  <p className="text-[10px] text-slate-500">Strike: {t.strike_pct_from_spot}x Spot</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm font-bold text-slate-200">${(t.premium_usd / 1000).toFixed(0)}k</p>
                <p className="text-[10px] text-slate-500">Premium</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
