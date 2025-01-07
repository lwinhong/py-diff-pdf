import subprocess
import os
import threading

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建exe文件的完整路径
exe_path = os.path.join(current_dir, "libs", "diff-pdf.exe")


def compare_pdfs(
        pdf1_path: str, pdf2_path: str, output_path: str = None, pages: str = None,
        progress_callback=None, compare_context=None, **kwargs,
):
    """
    比较两个PDF文件并生成差异报告。

    Args:
        pdf1_path (str): 第一个PDF文件的路径。
        pdf2_path (str): 第二个PDF文件的路径。
        output_path (str, optional): 输出差异报告的路径。如果未指定，则默认为'diff.pdf'。默认为None。
        pages (str, optional): 需要比较的PDF页码范围，格式为'1,2,6'。默认为None。
        progress_callback: 进度回调
        compare_context:配置项

    Returns:
        dict: 包含操作结果的字典。
            - output_path (str): 结果文档路径
            - success (bool): 操作是否成功。
            - message (str, optional): 如果操作失败，则返回错误信息；否则为None。

    Raises:
        FileNotFoundError: 如果pdf1_path或pdf2_path或者exe_path指定的文件不存在，则引发此异常。

    """
    # 如果exe文件不存在，抛出异常
    if not os.path.exists(exe_path):
        raise FileNotFoundError("diff-pdf.exe not found at {}".format(exe_path))

    # 校验输入参数是否为有效路径
    if not os.path.exists(pdf1_path):
        raise FileNotFoundError(f"pdf1_path not found: {pdf1_path}")

    if not os.path.exists(pdf2_path):
        raise FileNotFoundError(f"pdf2_path not found: {pdf2_path}")

    if output_path is None:
        output_path = os.path.join(current_dir, "diff.pdf")

    command = [
        exe_path,
        f"--output-diff={output_path}",
        pdf1_path,
        pdf2_path,
    ]
    if pages is not None:
        command.insert(2, f"--pages={pages}")

    # 启动进程
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    err_list = []

    def read_output(pipe, func):
        if func is not None:
            for line in iter(pipe.readline, ''):
                if compare_context is not None and compare_context.get("canceled", False):
                    process.terminate()
                    break

                line_str = line.strip()
                if line_str is not None and line_str.startswith('Progress:'):
                    [page, total] = line_str[len('Progress:'):].split(',')
                    func({
                        "page": int(page.strip()),
                        "total": int(total.strip())
                    })
                else:
                    err_list.append(line_str)

        pipe.close()

    # 实时读取标准输出和标准错误
    stdout_thread = threading.Thread(target=read_output, args=(process.stdout, progress_callback))
    stderr_thread = threading.Thread(target=read_output, args=(process.stderr, progress_callback))

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    # 获取返回码
    return_code = process.wait()
    # 等待进程结束并获取返回码

    success = return_code == 1  # 通常成功返回 1

    result = {
        "success": success,
        "message": '/n'.join(err_list) if not success and len(err_list) > 0 else '',
        "output_path": output_path
    }
    return result
