// Mermaid support for all pages
document.addEventListener('DOMContentLoaded', function() {
  // Check if there are any mermaid code blocks on the page
  const mermaidBlocks = document.querySelectorAll('pre.code mermaid, pre.mermaid, div.mermaid');
  if (mermaidBlocks.length > 0) {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
    script.onload = function() {
      mermaid.initialize({ startOnLoad: true });
    };
    document.head.appendChild(script);
  }
});
