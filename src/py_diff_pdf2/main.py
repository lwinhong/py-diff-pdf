import subprocess
import os

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建exe文件的完整路径
exe_path = os.path.join(current_dir, "libs", "diff-pdf.exe")


def compare_pdfs(
        pdf1_path: str, pdf2_path: str, output_path: str = None, pages: str = None
):
    """
    比较两个PDF文件并生成差异报告。

    Args:
        pdf1_path (str): 第一个PDF文件的路径。
        pdf2_path (str): 第二个PDF文件的路径。
        output_path (str, optional): 输出差异报告的路径。如果未指定，则默认为'diff.pdf'。默认为None。
        pages (str, optional): 需要比较的PDF页码范围，格式为'1,2,6'。默认为None。

    Returns:
        dict: 包含操作结果的字典。

            - success (bool): 操作是否成功。
            - message (str, optional): 如果操作失败，则返回错误信息；否则为None。

    Raises:
        FileNotFoundError: 如果pdf1_path或pdf2_path指定的文件不存在，则引发此异常。

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
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )

    try:
        # 循环读取标准输出
        for line in process.stdout:
            print(line, end="")  # 打印输出并保持与原始输出相同的格式

        # 获取标准错误输出（如果有的话）
        stderr_output = process.stderr.read()

        # 等待进程结束并获取返回码
        return_code = process.wait()
        success = return_code == 1  # 通常成功返回0

        result = {
            "success": success,
            "message": stderr_output if not success else None,
            "output_path": output_path
        }
        return result
    finally:
        # 确保流被关闭
        process.stdout.close()
        process.stderr.close()
