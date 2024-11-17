class UIController:
    def __init__(self):
        self.ui_elements = []  # 등록된 UI 요소를 저장

    def add_ui_element(self, element):
        """UI 요소 추가"""
        self.ui_elements.append(element)

    def update(self):
        """등록된 모든 UI 요소 업데이트"""
        for element in self.ui_elements:
            if hasattr(element, 'update'):
                element.update()

    def draw(self):
        """등록된 모든 UI 요소 렌더링"""
        for element in self.ui_elements:
            if hasattr(element, 'draw'):
                element.draw()
