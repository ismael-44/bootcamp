import os
import sys
import logging
import psutil
import math
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Defining log location
LOG_FILE = '/var/log/irondome.log'

#Extensions management list
extensions = [
'123', '3dm', '3ds', '3g2', '3gp', '602', '7z', 'arc', 'csv', 'doc', 'docx', 'dot', 'dotm', 'dotx', 'dwg', 'dxf',
'flv', 'gif', 'hwp', 'iso', 'iv2i', 'jpg', 'jpeg', 'lay', 'mdb', 'mdf', 'mid', 'moneywell', 'mov', 'mp3', 'mp4',
'mpeg', 'msg', 'myd', 'nef', 'odb', 'odg', 'odp', 'ods', 'odt', 'ora', 'paq', 'pdf', 'pef', 'pfx', 'php', 'png',
'pot', 'potm', 'potx', 'ppam', 'pps', 'ppsm', 'ppsx', 'ppt', 'pptm', 'pptx', 'psd', 'rar', 'raw', 'rtf', 'sql',
'sr2', 'srt', 'svg', 'swf', 'tar', 'tiff', 'txt', 'vbx', 'vsd', 'wav', 'wma', 'wmv', 'xla', 'xlam', 'xls', 'xlsb',
'xlsm', 'xlsx', 'xlt', 'xltm', 'xltx', 'xml', 'zip'
]
requested_extensions = []


# Init log
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IronDomeHandler(FileSystemEventHandler):
    
    def on_modified(self, event):
        path = event.src_path
        ext = path.split(".")[1:]
        if not requested_extensions:
            for a in ext:
                if a in extensions:
                    file_entropy = calculate_entropy(path)
                    if file_entropy < 5:
                        logging.warning(f'Entropy change detected in file: {path}')
        else:
            for a in ext:
                if a in requested_extensions:
                    file_entropy = calculate_entropy(path)
                    if file_entropy < 5:
                        logging.warning(f'Entropy change detected in file: {path}')
                
    def on_disk_usage(self):
        total_usage = psutil.disk_usage('/')
        if total_usage.percent >= 90:
            logging.warning('Abuse in disk read detected: Disk usage exceeds 90%')

    def on_crypto_activity(self):
        processes = psutil.process_iter(attrs=['name'])
        crypto_processes = [p.info['name'] for p in processes if 'crypto' in p.info['name']]
        if len(crypto_processes) > 3:
            logging.warning('Intensive cryptographic activity detected')

    def on_created(self, event):
        # Verificar si el evento es de creación de un archivo
        path = event.src_path
        ext = path.split(".")[1:]
        if not requested_extensions:
            for a in ext:
                if a in extensions:
                    logging.warning(f'Created file detected {event.src_path}')
        else:
            for a in ext:
                if a in requested_extensions:
                    logging.warning(f'Created file detected {event.src_path}')

    def on_deleted(self, event):
        # Verificar si el evento es de eliminación de un archivo
        path = event.src_path
        ext = path.split(".")[1:]
        if not requested_extensions:
            for a in ext:
                if a in extensions:
                    logging.warning(f'Delete file detected {event.src_path}')
        else:
            for a in ext:
                if a in requested_extensions:
                    logging.warning(f'Delete file detected {event.src_path}')

#Entropy calculation
def calculate_entropy(path):
    with open(path, 'rb') as file:
        content = file.read()
        byte_count = len(content)
        frequencies = [content.count(byte) for byte in range(256)]
        probabilities = [frequency / byte_count for frequency in frequencies]
        entropy = -sum(p * math.log2(p) if p != 0 else 0 for p in probabilities)
    return entropy

def calculate_entropy(path):
    with open(path, 'rb') as file:
        content = file.read()
        byte_count = len(content)
        if byte_count == 0:
            print(f"Skipping entropy of {path}. Empty file")
            return 0
        frequencies = [content.count(byte) for byte in range(256)]
        probabilities = [frequency / byte_count for frequency in frequencies]
        entropy = -sum(p * math.log2(p) if p != 0 else 0 for p in probabilities)
    return entropy


#Are you root
def youroot():
    if os.geteuid() != 0:
        print('You should be root...')
        sys.exit(1)

#Filter if path is correct
def filter_path(path):
    if not os.path.exists(path):
        print("Introduced path does not exist")
        exit()
    elif not os.path.isdir(path):
        print("The selected path is not a directory")
        exit()

#Filter user input
def argsparser():
    if len(sys.argv) == 1:
        print("Introduce at least one argument")
        exit()

    elif len(sys.argv) == 2:
        print("Using all extensions")
        path = sys.argv[1]
        filter_path(path)

    elif len(sys.argv) > 2:
        print("Using selected extensions")
        path = sys.argv[1]
        filter_path(path)
        arguments = sys.argv[2:]
        for a in arguments:
            if a in extensions:
                requested_extensions.append(a)
            else:
                print("Skipping", a,"unrecognized extension")
        print(requested_extensions)
    return path

#Start of main
def main():

    path = argsparser()

    observer = Observer()

    event_handler = IronDomeHandler()

    observer.schedule(event_handler, path=path, recursive=True)

    #Start monitoring
    observer.start()

    try:
        while True:
            event_handler.on_disk_usage()
            event_handler.on_crypto_activity()

            process = psutil.Process(os.getpid())
            if process.memory_info().rss >= 100 * 1024 * 1024:  # 100 MB en bytes
                logging.error('Memory usage exceeded 100 MB')
                sys.exit(1)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    main()
