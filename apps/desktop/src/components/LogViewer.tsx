import { Terminal } from 'lucide-react'
import { cn } from '../lib/utils'
import { TelemetryEvent } from '../hooks/useTelemetry'

interface LogViewerProps {
  events: TelemetryEvent[]
}

export function LogViewer({ events }: LogViewerProps) {
  const getEventColor = (event: TelemetryEvent) => {
    const phase = event.phase.toLowerCase()
    const type = event.event_type.toLowerCase()

    if (phase === 'repairing' || phase === 'rollback' || phase === 'failed' || type === 'error') {
      return 'text-rose-500' // Red
    }
    if (phase === 'bootstrapping' || phase === 'executing') {
      return 'text-emerald-500' // Green
    }
    if (phase === 'planning' || phase === 'validating' || phase === 'completed' || phase === 'idle') {
      return 'text-blue-500' // Blue
    }
    return 'text-slate-400'
  }

  return (
    <section className="md:col-span-2 flex flex-col gap-4">
      <div className="flex items-center gap-2 text-muted-foreground mb-2">
        <Terminal className="w-4 h-4" />
        <h2 className="text-sm font-semibold uppercase tracking-widest">Execution Telemetry</h2>
      </div>
      <div className="flex-1 bg-black/50 rounded-lg border border-border p-4 font-mono text-xs overflow-y-auto min-h-[400px]">
        {events.length === 0 ? (
          <span className="text-muted-foreground italic">Waiting for execution cycles...</span>
        ) : (
          events.map((event, i) => (
            <div key={i} className="mb-1.5 animate-in fade-in slide-in-from-left-1 duration-300">
              <span className="text-slate-600 mr-2 text-[10px]">
                {new Date(event.timestamp).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}
              </span>
              <span className={cn("mr-2 font-bold uppercase text-[10px]", getEventColor(event))}>
                [{event.phase}]
              </span>
              <span className="text-slate-300">{event.message}</span>
              {Object.keys(event.data).length > 0 && (
                <div className="ml-24 text-[10px] text-slate-500 italic">
                  {JSON.stringify(event.data)}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </section>
  )
}
