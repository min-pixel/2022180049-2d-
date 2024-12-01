class UIController:
    def __init__(self):
        self.ui_elements = []  # UI 요소 관리

    def add_ui_element(self, element):
        """UI 요소 추가"""
        self.ui_elements.append(element)

    def update(self):
        """활성화된 UI 요소 업데이트"""
        for element in self.ui_elements:
            if hasattr(element, 'update') and element.is_active:
                element.update()

    def draw(self):
        """UI 요소 렌더링"""
        for element in self.ui_elements:
            if hasattr(element, 'draw'):
                element.draw()

    def handle_event(self, e):
        """UI 요소에 이벤트 전달"""
        for element in self.ui_elements:
            if hasattr(element, 'handle_event') and element.is_active:
                if element.handle_event(e):
                    return True  # 이벤트 처리 완료
        return False
