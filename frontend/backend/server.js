const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const app = express();
const cors = require('cors');
const port = 3000;
const { spawn } = require('child_process');
const { pipeline } = require('stream');
const { StringDecoder } = require('string_decoder');

app.use(cors());
// 设置存储上传文件的目录
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadPath = `../upload/${req.query.type}`;
        if (!fs.existsSync(uploadPath)){
            fs.mkdirSync(uploadPath, { recursive: true });
        }
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({ storage: storage });

app.post('/upload', upload.single('file'), (req, res) => {
    res.json({ message: '文件上传成功' });
});

/*
app.get('/evaluate', (req, res) => {
    console.log("evaluate");
    exec('conda run -n emotion --live-stream python main.py',(error,stdout,stderr) => {
        if (error) {
            console.error(`执行出错: ${error.message}`);
            // 检查stderr以获取更详细的错误信息（如果可用）
            if (stderr) {
                console.error(`stderr: ${stderr}`);
            }
            return res.status(500).json({ message: '评估失败' });
        }
        console.log("finish exec");
        res.json({ message: stdout});
    });
    exec('python testjs.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`执行出错: ${error.message}`);
            // 检查stderr以获取更详细的错误信息（如果可用）
            if (stderr) {
                console.error(`stderr: ${stderr}`);
            }
            return res.status(500).json({ message: '评估失败' });
        }
        console.log(stdout);
        console.log("finish stdout");
        res.json({ message: stdout});
    });
    // exec('python testjs.py', (error, stdout, stderr) => {
    //     if (error) {
    //         console.error(`执行出错: ${error.message}`);
    //         // 检查stderr以获取更详细的错误信息（如果可用）
    //         if (stderr) {
    //             console.error(`stderr: ${stderr}`);
    //         }
    //         return res.status(500).json({ message: '评估失败' });
    //     }
    //     console.log(stdout);
    //     console.log("finish stdout");
    //     res.json({ message: stdout});
    // });
});
*/
app.get('/evaluate', (req, res) => {
    console.log("evaluate");
 
    const pythonProcess = spawn('conda', ['run', '-n', 'emotion', '--live-stream', 'python', 'main.py']);
 
    let decoder = new StringDecoder('utf8');
    let chunks = [];
 
    pythonProcess.stdout.on('data', (data) => {
        chunks.push(decoder.write(data));
    });
 
    pythonProcess.stdout.on('end', () => {
        chunks.push(decoder.end());
        const fullOutput = chunks.join('');
        console.log("finish exec");
        res.json({ message: fullOutput });
    });
 
    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${decoder.write(data)}`);
    });
 
    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Python process exited with code ${code}`);
            return res.status(500).json({ message: '评估失败' });
        }
    });
 
    pythonProcess.on('error', (error) => {
        console.error(`执行出错: ${error.message}`);
        return res.status(500).json({ message: '评估失败' });
    });
});

app.listen(port, () => {
    console.log(`服务器运行在 http://localhost:${port}`);
});