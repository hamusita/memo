from multiprocessing import Process
from multiprocessing.managers import SharedMemoryManager

def func1(shm, arg):
    shm.buf[0] = arg
    shm.close()

if __name__ == '__main__':

    # 共有メモリ管理プロセスを起動
    with SharedMemoryManager() as smm:

        # 共有メモリを作成し、初期値を設定
        shm1 = smm.SharedMemory(10)  
        shm1.buf[0] = 0

        # func1を異なるプロセスで起動
        p1 = Process(target=func1, args=(shm1, 100))

        # func1を異なるプロセスで起動
        p2 = Process(target=func1, args=(shm1, 200))

        p1.start()
        p2.start()

        p1.join()
        p2.join()
        
        print(shm1.buf[0])