from typing import Dict, List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from rank_bm25 import BM25Okapi


class SkeletonSummaryMessage(BaseMessage):
    def __init__(self, content: str, meta: dict = None):
        super().__init__(content=content)
        self.role = 'summary'
        self.meta = meta or {}
        
    @property
    def type(self) -> str:
        return self.role
    
    def __str__(self):
        return f"[{self.role.upper()}@SKELETONSTEP] {self.content}"
    
    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "meta": self.meta
        }



class FullInputMemory(BaseChatMessageHistory):
    def __init__(self, max_prompt_history: int = 2):
        self.full_history: List[Dict] = []  
        self.messages: List[BaseMessage] = []  
        self.max_prompt_history = max_prompt_history

    @property
    def memory_variables(self):
        return ["history"]

    def load_memory_variables(self, inputs: Dict):
        query = inputs.get("feedback", "")
        
        if len(self.messages) <= self.max_prompt_history:
            final_msgs = self.messages
        else:
            last_msg = self.messages[-1]
            middle_msgs = self.messages[:-1]
            
            corpus = [msg.meta.get("feedback","") for msg in middle_msgs]
            
            tokenized_corpus = [doc.split(" ") for doc in corpus]
            bm25 = BM25Okapi(tokenized_corpus)
            
            tokenized_query = query.split()
            scores = bm25.get_scores(tokenized_query)
            middle_limit = self.max_prompt_history - 1
            ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
            top_indices = ranked_indices[:middle_limit]
            
            related_middle_msgs = [middle_msgs[i] for i in sorted(top_indices)]
            
            selected_msgs = related_middle_msgs + [last_msg]
            selected_msgs.sort(key=lambda m: m.meta.get("step", None))
            
            final_msgs = []
            prev_step = None
            for idx, msg in enumerate(selected_msgs):
                step = msg.meta.get("step", None)
                if idx == 0 and step is not None and step > 1:
                    skip_text = f"[...skipping steps 1 to {step - 1}...]"
                    final_msgs.append(SkeletonSummaryMessage(content=skip_text, meta={"step": ' '}))
                if prev_step is not None and step is not None and step - prev_step > 1:
                    skip_text = f"[...skipping steps {prev_step + 1} to {step - 1}...]"
                    final_msgs.append(SkeletonSummaryMessage(content=skip_text, meta={"step": ' '}))
                
                final_msgs.append(msg)
                prev_step = step
        
        return {"history": "\n".join([str(m) for m in final_msgs])}
        

    def save_context(self, inputs: Dict, outputs: Dict):
        self.full_history.append({
            "inputs": inputs,
            "outputs": outputs
        })
        step = len(self.full_history)  

        if step == 1:
            self.messages.append(SkeletonSummaryMessage(content=f"Generated Skeleton:\n{str(outputs.get('result',''))}", meta={"step": step}))
        elif step > 1:
            self.messages.append(SkeletonSummaryMessage(content=f"The feedback of the STEP {step-1} is:\n{inputs.get('feedback','')}\nGiven the feedback of STEP {step-1}, the diff between the updated skeleton and the previous skeleton is:\n{outputs.get('skeleton_diff','')}\n", meta={"step": step, "feedback": inputs.get("feedback","")}))

    def clear(self):
        self.full_history.clear()
        self.messages.clear()
        
    def add_message(self, message: BaseMessage):
        self.messages.append(message)

    def add_messages(self, messages: list[BaseMessage]):
        self.messages.extend(messages)

class GlobalMemoryManager:
    _histories: Dict[str, FullInputMemory] = {}

    @classmethod
    def get(cls, session_id: str, max_prompt_history: int = 2) -> FullInputMemory:
        if session_id not in cls._histories:
            cls._histories[session_id] = FullInputMemory(max_prompt_history=max_prompt_history)
        return cls._histories[session_id]

    @classmethod
    def clear(cls, session_id: str):
        if session_id in cls._histories:
            cls._histories[session_id] = FullInputMemory(
                max_prompt_history=cls._histories[session_id].max_prompt_history
            )

    @classmethod
    def all_histories(cls) -> Dict[str, FullInputMemory]:
        return cls._histories


def get_session_history(session_id: str, max_prompt_history: int = 2) -> FullInputMemory:
    return GlobalMemoryManager.get(session_id, max_prompt_history=max_prompt_history)
