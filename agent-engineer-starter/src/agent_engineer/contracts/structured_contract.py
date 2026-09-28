from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError
class TicketResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    category: Literal["billing","technical","other"]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str = Field(min_length=1, max_length=300)
    priority: Literal["low","medium","high","urgent"] = "medium"
def validate_ticket_output(raw_output: str) -> tuple[bool,str|None,TicketResult|None]:
    try: return True,None,TicketResult.model_validate_json(raw_output)
    except ValidationError as exc:
        errors=[]
        for err in exc.errors():
            loc=".".join(str(x) for x in err["loc"]); errors.append(f"字段 '{loc}': {err['msg']}")
        return False,"输出未通过 Schema 校验，请修正 JSON：\n"+"\n".join(errors),None
    except Exception as exc: return False,f"JSON 解析失败: {exc}",None
