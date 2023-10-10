function promiseReadFile(file: File): Promise<ArrayBuffer> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onerror = (event): void => {
      reject(event);
    };
    reader.onload = (event): void => {
      if (event.target === null || event.target.result === null) {
        reject(new Error("event.target is null"));
        return;
      }
      if (typeof event.target.result === 'string') {
        reject(new Error("event.target.result is a string"));
        return;
      }
      resolve(event.target.result as ArrayBuffer);
    };
  });
}

export { promiseReadFile };
