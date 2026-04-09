import { type RefObject } from "react";
import CameraCapture from "./CameraCapture";

interface Props {
  videoRef: RefObject<HTMLVideoElement | null>;
  cameraReady: boolean;
  snapshot: string | null;
  showSnapshot: boolean;
}

export default function VisitorPanel({
  videoRef,
  cameraReady,
  snapshot,
  showSnapshot,
}: Props) {
  return (
    <div style={container}>
      <div style={videoWrap}>
        <CameraCapture videoRef={videoRef} ready={cameraReady} />
        {showSnapshot && snapshot && (
          <img
            src={snapshot}
            alt=""
            style={{
              position: "absolute",
              inset: 0,
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: "scaleX(-1)",
            }}
          />
        )}
      </div>
      <div style={labelBar}>
        <span style={labelText}>VISITOR</span>
      </div>
    </div>
  );
}

const container: React.CSSProperties = {
  position: "relative",
  display: "flex",
  flexDirection: "column",
  height: "100%",
  background: "#000",
  overflow: "hidden",
};

const videoWrap: React.CSSProperties = {
  position: "relative",
  flex: 1,
  overflow: "hidden",
};

const labelBar: React.CSSProperties = {
  padding: "8px 16px",
  background: "var(--color-surface)",
  borderTop: "1px solid #222",
};

const labelText: React.CSSProperties = {
  fontFamily: "var(--font-mono)",
  fontSize: 10,
  letterSpacing: "0.12em",
  color: "var(--color-text-dim)",
  textTransform: "uppercase",
};
