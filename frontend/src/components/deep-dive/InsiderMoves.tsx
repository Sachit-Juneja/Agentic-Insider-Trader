import { FinalReport } from "@/lib/types";
import { Card } from "@/components/ui/card";

export function InsiderMoves({ report }: { report: FinalReport }) {
  const data = report?.insider_highlights;
  if (!data) return <div className="text-slate-500">No insider data available.</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <Card className="bg-[#0a0e27] border-slate-800 p-4">
          <h4 className="text-xs text-slate-500 font-bold uppercase mb-2">Net Sentiment</h4>
          <p className={`text-xl font-black ${data.net_sentiment === 'bullish' ? 'text-[#00ff88]' : 'text-[#ff3366]'}`}>
            {data.net_sentiment?.toUpperCase() || 'NEUTRAL'}
          </p>
        </Card>
        <Card className="bg-[#0a0e27] border-slate-800 p-4">
          <h4 className="text-xs text-slate-500 font-bold uppercase mb-2">Form 4 Filings</h4>
          <p className="text-xl font-black text-slate-200">{data.form4_count} Recent</p>
        </Card>
      </div>

      <div>
        <h4 className="text-[#00d4ff] font-bold uppercase mb-3 border-b border-slate-800 pb-2">Recent Insider Trades</h4>
        <div className="space-y-2">
          {data.filings?.map((f: any, i: number) => (
            <div key={i} className="flex justify-between items-center p-3 bg-[#0d1333] border border-slate-800 rounded">
              <div>
                <p className="text-sm font-bold text-slate-200">{f.insider_name}</p>
                <p className="text-[10px] text-slate-500">{f.insider_title} • {f.filing_date}</p>
              </div>
              <div className="text-right">
                <p className={`text-sm font-bold ${f.transaction_type === 'Purchase' ? 'text-[#00ff88]' : 'text-[#ff3366]'}`}>
                  {f.transaction_type}
                </p>
                <p className="text-[10px] text-slate-400">{f.shares?.toLocaleString()} shs @ ${f.price_per_share}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {data.congressional?.length > 0 && (
        <div>
          <h4 className="text-[#00d4ff] font-bold uppercase mb-3 border-b border-slate-800 pb-2">Congressional Trades</h4>
          <div className="space-y-2">
            {data.congressional.map((c: any, i: number) => (
              <div key={i} className="flex justify-between items-center p-3 bg-[#0d1333] border border-slate-800 rounded">
                <div>
                  <p className="text-sm font-bold text-slate-200">{c.member} ({c.party})</p>
                  <p className="text-[10px] text-slate-500">{c.role} • {c.disclosure_date}</p>
                </div>
                <div className="text-right">
                  <p className={`text-sm font-bold ${c.transaction_type === 'Purchase' ? 'text-[#00ff88]' : 'text-[#ff3366]'}`}>
                    {c.transaction_type}
                  </p>
                  <p className="text-[10px] text-slate-400">{c.amount_range}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
