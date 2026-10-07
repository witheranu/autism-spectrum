import { cn } from "@/lib/utils";

interface ConversationBubbleProps {
  text: string;
  speaker: string;
  isCurrentUser: boolean; // to determine left/right alignment
  timestamp: string;
}

export function ConversationBubble({ text, speaker, isCurrentUser, timestamp }: ConversationBubbleProps) {
  return (
    <div className={cn("flex w-full mt-4 space-x-3 max-w-2xl", isCurrentUser ? "ml-auto justify-end" : "")}>
      {!isCurrentUser && (
        <div className="flex-shrink-0 mt-1 w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-xs font-semibold text-slate-500">
          {speaker.charAt(0)}
        </div>
      )}
      <div>
        <div className={cn("p-3 rounded-2xl", isCurrentUser ? "bg-primary text-primary-foreground rounded-br-sm" : "bg-muted rounded-bl-sm")}>
          <p className="text-sm">{text}</p>
        </div>
        <span className={cn("text-xs text-muted-foreground mt-1 flex", isCurrentUser ? "justify-end" : "justify-start")}>
          {speaker} • {new Date(timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
        </span>
      </div>
      {isCurrentUser && (
        <div className="flex-shrink-0 mt-1 w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-xs font-semibold text-primary">
          {speaker.charAt(0)}
        </div>
      )}
    </div>
  );
}
