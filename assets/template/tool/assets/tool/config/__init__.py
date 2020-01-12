import os;
import json;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));

# 工具信息
TOOL_INFO = {};
def initToolInfo():
    toolPath = os.path.join(CURRENT_PATH, "../tool.json");
    if os.path.exists(toolPath):
        with open(toolPath, "r") as f:
            TOOL_INFO = json.loads(f.read());
initToolInfo();