// 切片上传大文件测试
(() => {
    const btn = document.querySelector('#uploadBtn');
    let xhr;

    btn.addEventListener('click', () => {
        if (xhr) {
            xhr.abort();
            xhr = null;
            return;
        }
        const fileObj = document.querySelector('#fileInput').files[0];
        const { size } = fileObj;
        const partSize = 50 * 1024 * 1024;
        let curSize = 0;
        const upload = cutUpload();
        upload.next();

        function* cutUpload() {
            while (curSize < size) {
                console.log(curSize + partSize, size)
                const nextSize = Math.min(curSize + partSize, size)
                const cutFile = fileObj.slice(curSize, nextSize);
                const reader = new FileReader();

                reader.readAsArrayBuffer(cutFile);
                reader.onload = (e) => {
                    xhr = new XMLHttpRequest();
                    xhr.open('POST', `/upload?s=${curSize}&t=${size}&f=${fileObj.name}`);
                    xhr.setRequestHeader('Content-Type', 'application/octet-stream');
                    xhr.send(e.target.result);

                    xhr.onreadystatechange = () => {
                        if (xhr.readyState == 4){
                            try {
                                const res = JSON.parse(xhr.response);
                                console.log(res);
                                upload.next();
                            } catch(e) {}
                        }
                    };
                    curSize += cutFile.size;
                };
                yield;
            }
            xhr = null;
        }
    }, false);
})();

// socket测试
(() => {
    const ws = new WebSocket("ws://localhost:1236/socket/test");

    ws.onmessage = (evt) => {
        console.log(evt.data);
    };
    document.querySelector('h2').addEventListener('click', () => {
        ws.send("comming");
    }, false);
})();