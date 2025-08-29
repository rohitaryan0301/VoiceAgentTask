import React from 'react';

export default function Home() {
  return (
    <div style={{fontFamily:'sans-serif',padding:40}}>
      <h1>AI Voice Agent — Frontend (placeholder)</h1>
      <p>This is a simple placeholder. Replace with your actual Next.js frontend.</p>
      <p>API base: <code>{process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}</code></p>
    </div>
  );
}
