1차 발표: https://youtu.be/Nr-rIA4Na6w  
게임의 간단한 소개 (카피의 경우 원작에 대한 언급)  
  뱀파이어 서바이벌 장르의 게임  
게임 컨셉, 핵심 메카닉 제시
  게임의 컨셉 : 귀여운 포켓몬(피츄)가 야생에서 살아남는 뱀파이어 서바이벌 장르의 게임.
  캐릭터 이동 : 방향키의 8방향 조작  
  적 생성 및 패턴: 시간이 지날수록 점점 많은 적이 등장, 적의 종류에 따라 체력, 속도를 다르게  
  업그레이드 시스템: 적을 처치하면 경험치를 얻고, 레벨업할 때마다 무기나 스킬을 선택해 캐릭터를 강화  
스크린샷 혹은 그림판으로 끄적인 이미지 포함  
  ![image](https://github.com/user-attachments/assets/9e21164e-9f7c-4b2b-a63d-f337bb71ddc4)

예상 게임 실행 흐름
1. 플레이어는 방향키를 사용하여 이동하며, 제한 시간 동안 다가오는 적을 피하거나 처치하며 생존.
2. 적에게 부딪히면 즉시 게임 종료.
3. 플레이어는 기본 공격(투사체 발사)을 자동으로 하며, 적은 시간이 지날수록 더 많이 더 강하게 등장.
4. 적을 처치하면 경험치 획득 → 경험치를 모아 레벨업 시 스킬 선택 가능 (3개의 스킬 중 하나 선택).
  스킬 종류:
    슬로우: 투사체를 맞은 적을 느리게 만듦.
    관통: 투사체가 여러 적을 관통하여 경로상의 모든 적에게 데미지.
    쉴드: 플레이어 주변을 돌며 적의 공격을 막아주는 보호막 형태의 강화된 투사체를 생성합니다.
5. 플레이어는 최대 3레벨까지 성장 가능.
6. 적의 종류:
    체력이 많고 느리게 움직이는 적.
    체력이 적고 빠르게 움직이는 적.

개발 내용  
Scene 의 종류 및 구성, 전환 규칙  
  타이틀 씬  
  ![image](https://github.com/user-attachments/assets/5aa3e1aa-b901-4fd5-ae23-c29c177ec91d)  
  로딩 씬  
  ![image](https://github.com/user-attachments/assets/d4fd2d3a-c91f-478a-b7d0-a40b32199a9a)  
  플레이 씬  
  ![image](https://github.com/user-attachments/assets/3a3c4628-0f0a-47fd-89d0-2a010eb70cd8)  
  ![image](https://github.com/user-attachments/assets/7e9e88a6-7916-4d26-9ee2-321203e59e80)  
  
각 Scene 에 등장하는 GameObject 의 종류 및 구성, 상호작용  
  타이틀 씬  
    1. 배경 이미지  
    2. 게임 제목  
    3. 깜빡이는 Press Button 텍스트  
  로딩 씬  
    1. 배경 이미지  
    2. '로딩 중..' 텍스트  
    3. 얼만큼 로딩이 진행됐는지 보여주는 로딩 바  
    
  플레이 씬 (main_game_scene) 
    1. 플레이어  
    2. 플레이어가 쏘는 투사체  
    3. 적01  
    4. 적02 
    5. 적03
    6. 적04
    7. 경험치 아이템  
    8. 레벨 게이지  
    9. 타이머  
    10. 스킬 트리 UI  
  
모든 class 에 대한 언급, 각 클래스의 역할을 나열, 생김새를 간단한 문장으로 표현  
  1. Player: 플레이어 캐릭터로,방향키를 통해 이동하고 자동으로 공격합니다.  
      간단한 2d이미지 캐릭터  
         ![image](https://github.com/user-attachments/assets/0f518885-3df4-4a1c-9ce2-760acf78cd1b)  
  2. Enemy: 플레이어를 공격하며, 종류에 따라 이동 속도와 체력이 다릅니다.  
       세모와 마름모같은 간단한 도형  
  3. Projectile(bullet): 플레이어의 기본 공격 수단이며 적을 타격합니다.  
       동그라미  
  4. SkillTree: 플레이어가 경험치를 모아 레벨업 시 스킬을 선택할 수 있도록 도와줍니다. 각 스킬은 투사체를 강화하는 효과가 있습니다.  
       화면에 등장하는 UI로, 선택 가능한 3개의 스킬 버튼이 표시됩니다.  
  5. ExperienceItem (경험치 아이템): 적을 처치했을 때 떨어지며, 플레이어가 획득 시 경험치 증가.  
       육각형의 도형  

화면에 보이지 않는 Controller 객체들에 대한 언급  
  1. EnemySpawner: 적의 생성 주기를 관리하며, 시간이 지남에 따라 더 많은 적을 생성합니다.  
  2. ExperienceManager: 플레이어가 경험치 아이템을 먹었을 때 경험치를 추가하고, 레벨업을 판단합니다.    ------>    필수적이지 않은 기능적 분리보다는 빠른 기능 완성을 목표로 하기위해 파기.
  3. UIController: 경험치 바와 타이머 등 UI 요소를 관리합니다.
  4. bullet_Manager: 플레이어의 기본 공격 수단에 대한 처리를 관리합니다. (가까운 적 객체 방향으로 쏘기, 1초마다 자동으로 쏘기)  

함수 단위의 설명 (1차발표때는 아직 알 수 없을 것이므로, 2차발표때 추가)  
  플레이 씬 (main_game_scene) 
  1. 플레이어 (boy) 
   - **구성 정보**: 이미지![PokemonPlayer](https://github.com/user-attachments/assets/20431fa6-0850-4bab-a4fa-ec02a6bc7c17)
를 사용하는 2D 캐릭터로, 방향키로 8방향 이동 가능.
프레임 기반 애니메이션으로, 8개의 프레임과 두 줄로 구성된 이미지에서 방향과 동작에 따라 다른 클립을 표시.
   - **상호작용 정보**:  
     - 경험치 아이템과 충돌 시 경험치를 획득하고 레벨 업 가능.  
     - 적과 충돌 시 게임 종료.  
   - **핵심 코드 설명**:  
     ```python
     def update(self):
         self.x += self.dx * self.speed * self.mag * gfw.frame_time
         self.y += self.dy * self.speed * self.mag * gfw.frame_time
     ```
    dx와 dy를 바탕으로 프레임 시간에 맞춰 위치를 계산. 
  2. 플레이어가 쏘는 투사체 (Bullet)
  - **구성 정보**: 이미지![bullet](https://github.com/user-attachments/assets/9ad73629-fcf6-448a-b2d4-9f154f0fd859)
  를 사용하는 플레이어가 쏘는 투사체. 발사된 위치와 방향, 속도에 따라 매 프레임마다 이동.
     - **상호작용 정보**:  
       - 적과 충돌 시 적의 체력을 감소.  
     - **핵심 코드 설명**:  
       ```python
       def update(self):
          self.x += self.direction[0] * self.speed * gfw.frame_time
          self.y += self.direction[1] * self.speed * gfw.frame_time
       ```
       총알의 이동 방향과 속도를 바탕으로 위치를 업데이트.
  3. 적 (Enemy ~ Enemy04)
        - **구성 정보**:
            기본 적 이미지: ![Enemy](https://github.com/user-attachments/assets/63e36a87-1111-4fa8-97c5-fa46803d9357)  
            Enemy02 이미지: ![Enemy02](https://github.com/user-attachments/assets/b90ce2aa-980d-46f4-8033-df53743fbab6)  
            Enemy03 이미지: ![Enemy03](https://github.com/user-attachments/assets/bf5f0f07-3e07-4d27-98ec-f095f5c03b47)  
            Enemy04 이미지: ![Enemy04](https://github.com/user-attachments/assets/cfb65940-2086-4639-abea-2333b128cfa6)  
  
          프레임 기반 애니메이션으로, 행동(왼쪽/오른쪽 이동)에 따라 프레임이 달라짐.  
          다양한 Enemy 클래스를 상속받아 체력과 속도가 다른 적 생성.  
     - **상호작용 정보**:  
       - 총알과 충돌 시 체력이 감소.
       - 체력이 0이 되면 사라지고 경험치 아이템 드랍.
       - BehaviorTree를 사용하여 플레이어를 추적하는 행동을 구현.
       - 플레이어와 부딪히면 게임 종료 (아직 미구현) 
     - **핵심 코드 설명**:  
       ```python
       def chase_player(self):
          dx = self.player.x - self.x
          dy = self.player.y - self.y
          distance = math.sqrt(dx**2 + dy**2)
          self.x += (dx / distance) * self.speed * gfw.frame_time
          self.y += (dy / distance) * self.speed * gfw.frame_time
       ```
       플레이어의 위치와의 거리(dx, dy)를 계산하여 적이 추적하도록 설정
  4. 경험치 아이템 (ExpItem)
        - **구성 정보**: 이미지![exp_item](https://github.com/user-attachments/assets/ba273faa-b0a6-444a-9e4b-b49b65d3b8da)
  를 사용하는 오브젝트. 일정한 경험치를 제공하며 플레이어가 충돌 시 소멸.
     - **상호작용 정보**:  
       - 적이 죽으면 드랍.
       - 플레이어와 닿으면 소멸 및 경험치 추가, 레벨 업 이벤트 
     - **핵심 코드 설명**:  
       ```python
       def handle_collision(self, player):
            if hasattr(player, 'level_bar'):
            leveled_up = player.level_bar.add_exp(self.amount)
            if leveled_up:
               player.level_up()
       ```
       플레이어와의 충돌 시 경험치를 추가하고, 레벨 업 조건을 만족하면 이벤트를 실행
  5. 레벨 게이지 (LevelBar)
       - **구성 정보**: 이미지![progress_bg02](https://github.com/user-attachments/assets/42ea57a9-2768-413b-a4f0-518650ac5b9d)와 ![progress_fg02](https://github.com/user-attachments/assets/e79f8d41-5645-44ec-a08b-1b09a249e106)
  를 사용하는 경험치 진행 바.
     - **상호작용 정보**:  
       - 경험치에 따라 진행률이 업데이트되며, 100%에 도달하면 레벨 업. (현재 레벨 업은 미구현)  
     - **핵심 코드 설명**:  
       ```python
          def add_exp(self, exp):
            self.progress += exp / self.max_exp
            if self.progress >= 1.0:
                self.progress = 1.0
                return True
            return False
       ```
       경험치가 최대치를 넘으면 레벨 업 이벤트를 반환.
  6. 타이머 (timer)
        - **구성 정보**: 시간 경과를 표시하는 텍스트 UI
     - **상호작용 정보**:  
       - 시간 경과에 따라 줄어드는 시간을 보여준다. (현재는 매 초 경과 시간을 계산하여 화면에 표시하는 중, 11/25 ~ 11/30 사이에 구현 예정)  
     - **핵심 코드 설명**: 
  7. 스킬 트리 UI  (아직 미구현)

 
사용한/사용할 개발 기법들에 대한 간단한 소개  
  1. 자동 타겟팅 시스템: 플레이어가 적을 자동으로 공격하는 시스템.  
  2. 경험치 기반 레벨업 시스템: 적을 처치하면 경험치를 얻고 레벨업 시 스킬을 선택하는 시스템.  
  3. pico2d와 gfw 프레임워크: 화면 렌더링, 게임 루프 관리, 객체 업데이트 등을 위한 프레임워크 사용.  
     
각 개발 요소들을 정량적으로 제시할 것  
  1. 적 등장 빈도: 5초마다 적의 등장 수가 1개씩 증가.
  2. 적의 종류: 4개까지
  3. 레벨업 경험치: 레벨 1에서 2로는 100 경험치, 레벨 2에서 3으로는 200 경험치 필요.
  4. 레벨업 아이템: 한개마다 레벨 수치 10씩 증가
  5. 플레이어의 공격 속도(디폴트): 1초마다 한번 자동공격
  6. 플레이어가 버텨야 하는 게임시간: 60초

게임 프레임워크  
프레임워크에서 지원되는 기능들 중 어떤 것을 사용할 것인지  
   1. pico2d를 사용해 화면 렌더링 및 입력 처리.  
   2. gfw 프레임워크를 사용해 씬 전환, 상태 관리.

아직 배우지 않았거나 다루지 않을 항목이 있는지   
  1.   

일정   
1주차 (10/28 - 11/3): 기본 시스템 구축 및 캐릭터 동작  
  목표: 게임의 기본 구조와 캐릭터 이동 기능 구현  
    타이틀, 로딩, 플레이 씬 구성: 씬 전환 기능과 UI 배치 설정  
    캐릭터 이동: 방향키를 통한 8방향 이동 구현  
2주차 (11/4 - 11/10): 자동 공격 시스템과 기본 투사체 구현
  목표: 플레이어의 자동 공격 기능 구현  
    투사체 발사 시스템: 플레이어가 자동으로 투사체를 발사하는 시스템  
    투사체와 적 간의 충돌 로직: 기본 타격 메커니즘 설정  
3주차 (11/11 - 11/17): 적 생성 시스템과 간단한 AI 구현  
  목표: 적의 등장과 기초 AI 설정  

    UI컨트롤러 제작(1, 2주차에서 미뤄짐)
    투사체와 적 간의 충돌 로직 (불렛매니저 구현에 시간을 많이 써서 2주차에서 미뤄짐)
    EnemySpawner 구현: 적 등장 주기 설정, 시간이 지날수록 등장 수 증가  
    기본 적 AI: 플레이어를 향해 이동하는 단순 패턴 설정  
    해결.

    
4주차 (11/18 - 11/24): 경험치 시스템과 레벨업 구현  
  목표: 적 처치 후 경험치 획득 및 레벨업 시스템 구현  
    경험치 아이템 생성 및 획득: 적 처치 시 경험치 아이템 드랍, 플레이어가 획득 시 경험치 증가  
    레벨업 조건 설정: 특정 경험치 도달 시 레벨업  
     종류에 따라 속도 및 체력 차별화(3주차에서 미뤄짐: 해결완료.)  
5주차 (11/25 - 12/1): 스킬 선택 시스템 구현  
  목표: 레벨업 시 스킬 선택 기능 추가  
    스킬 트리 UI 구현: 레벨업 시 3개의 스킬 중 하나를 선택할 수 있는 UI 구성  
    스킬 효과 추가: 슬로우, 관통, 쉴드 스킬 구현  
6주차 (12/2 - 12/8): 게임 오류 수정      
  목표: 시스템 통합 및 오류 제거  
    전체 기능 동작 확인 및 버그 수정  
6.5주차 (12/9 - 12/12): 최종 점검 및 보완  
  목표: 전체 시스템 점검 및 세부 조정  
    버그 수정 및 최종 테스트: 모든 기능의 통합 테스트 및 버그 수정  
    최종 발표 준비: 게임 화면 캡처, 데모 영상 제작, 발표 자료 준비  

## 주별 커밋 수 (GitHub Insights 기준)
| 주차       | 날짜 범위            |  커밋 수 |
|------------|---------------------|----------|
| 1주차      | 10/27 - 11/03       | 3        |
| 2주차      | 11/04 - 11/10       | 3        |
| 3주차      | 11/11 - 11/17       | 4        |
| 4주차      | 11/18 - 11/24       | 10       |
| 5주차      | 11/25 - 12/01       | 0        |
| 6주차      | 12/02 - 12/08       | 0        |

 
