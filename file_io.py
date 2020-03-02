import pickle
import os

def reset_memory():
    mem = load('assignments')
    mem = []
    save('assignments', mem)

def load(name):
    '''
    This method creates and loads a new journal.

    : param name: This base name of journal to load.
    : return: A new journal data structure populated with the file data.
    '''
    filename = get_full_pathname(name)
    data = None
    if os.path.exists(filename):
        with open(filename, 'rb') as fin:
            data = pickle.load(fin)
    return data


def save(name, data):
    filename = get_full_pathname(name)
    print("... saving to: {}".format(filename))
    with open(filename, 'wb') as file_out:
        pickle.dump(data, file_out, pickle.HIGHEST_PROTOCOL)


def get_full_pathname(name):
    filename = os.path.abspath(os.path.join('.',name + '.pkl'))
    return filename

if __name__ == "__main__":
    reset_memory()
