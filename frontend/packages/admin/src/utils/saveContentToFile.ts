export default function saveContentToFile(content: BlobPart, type: string, fileName: string): void {
  const blob = new Blob([content], { type });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  document.body.appendChild(link);
  link.href = url;
  link.download = fileName;
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}
