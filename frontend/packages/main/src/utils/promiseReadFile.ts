function promiseReadFile(file): Promise<ArrayBuffer> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onload = (event): void => {
      resolve(event.target.result);
    };
    reader.onerror = (event): void => {
      reject(event);
    };
  });
}

export { promiseReadFile };
