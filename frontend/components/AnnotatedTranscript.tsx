import { cn } from "@/lib/utils";

interface AnnotatedSpan {
  text: string;
  framing: "deficit" | "strength" | "neutral";
}

interface AnnotatedTranscriptProps {
  spans: AnnotatedSpan[];
}

export function AnnotatedTranscript({ spans }: AnnotatedTranscriptProps) {
  return (
    <div className="p-4 bg-white rounded-lg border leading-relaxed text-sm">
      {spans.map((span, idx) => {
        let bgColorClass = "";
        let textColorClass = "text-foreground";
        
        if (span.framing === "deficit") {
          bgColorClass = "bg-[var(--color-frame-deficit)]/40";
          textColorClass = "text-red-900 font-medium";
        } else if (span.framing === "strength") {
          bgColorClass = "bg-[var(--color-frame-strength)]/60";
          textColorClass = "text-green-900 font-medium";
        } else {
          bgColorClass = "bg-[var(--color-frame-neutral)]/20";
        }

        return (
          <span 
            key={idx} 
            className={cn("px-1 py-0.5 rounded-sm mx-0.5 transition-colors", bgColorClass, textColorClass)}
            title={`${span.framing} framing`}
          >
            {span.text}
          </span>
        );
      })}
    </div>
  );
}
