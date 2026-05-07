import { Shield } from 'lucide-react'

export function StatusCard() {
  return (
    <div className="p-4 bg-card rounded-xl border border-border">
      <div className="flex items-center gap-2 mb-4">
        <Shield className="w-5 h-5 text-primary" />
        <h3 className="font-bold">Safety Boundaries</h3>
      </div>
      <div className="space-y-3">
        <div className="flex justify-between items-center text-sm">
          <span className="text-muted-foreground">Sandbox Isolation</span>
          <span className="text-emerald-400 font-medium">Active</span>
        </div>
        <div className="flex justify-between items-center text-sm">
          <span className="text-muted-foreground">Network Containment</span>
          <span className="text-emerald-400 font-medium">Strict</span>
        </div>
        <div className="flex justify-between items-center text-sm">
          <span className="text-muted-foreground">Rollback Ready</span>
          <span className="text-primary font-medium">Initialized</span>
        </div>
      </div>
    </div>
  )
}
