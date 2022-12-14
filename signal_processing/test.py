import numpy as np
import matplotlib.pyplot as plt
# from scipy.fft import rfft,irfft


f=200*10**6
T=100*10**(-6)
f_cutoff=48*10**6
n=int(T*f)

t=np.linspace(0,T,n)
signal=np.sin(2*np.pi*f*t)
for i in range(n):
    signal[i]+=np.random.normal(0,1)

def sample(sample_f,f, amplitude, t_max):
    sample_f = int(sample_f)
    x = np.linspace(0,t_max,sample_f)
    y_ = np.zeros(sample_f)
    for i in range(sample_f):
        y_[i] = f(x[i], amplitude)
    return x, y_

# generate random values between -1 and 1
def random_values(sampling_f, total_length):
    length = int(sampling_f*total_length)
    noise = np.random.random(length)*2-1
    return noise

noise = random_values(200*10**6, 0.1)
print(np.shape(noise))


# Fiens solution

M=50
N=M+1 

fc = 0.24  # Cutoff frequency as a fraction of the sampling rate (=48 MHz/200MHz).
b = 0.08  # Transition band, as a fraction of the sampling rate (=4/N).
n50 = np.arange(N)

def sinc_Blackman(N,n):
    # Sinc filter.
    h = np.sinc(2 * fc * (n - (N - 1) / 2))
 
    # Blackman window.
    w = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
    # Multiply sinc filter by window.
    h = h * w
    # Normalize to get unity gain.
    h = h / np.sum(h)
    return h

h50=sinc_Blackman(51,n50)
plt.plot(n50,h50)
plt.xlabel("Sample number")
plt.ylabel("Impulse response")
plt.title("Impulse response")
plt.show()



signal_filtered50 = np.convolve(signal, h50)

print(np.shape(signal_filtered50))



# signal_filter_fourier50=np.fft.rfft(signal_filtered50)
# signal_filter_fourier50=signal_filter_fourier50.real
# # freq=rfft(t)
# # freq=freq.real
# plt.plot(signal_filter_fourier50[0:len(freq)])
# plt.xlabel("Frequency")
# plt.ylabel("Amplitude")
# plt.xlim(0,1)
# plt.show()



# my solution

Amp = np.zeros(len(noise))
Amp = np.zeros(26)

interest = int((48*10**6*0.1)/len(noise) * len(Amp))

Amp[0:interest] = 1

# check if the amplitude function looks right

# plt.figure()
# plt.plot(Amp)
# plt.title('Amplitude function; responsible for filtering')
# plt.show()


def h_of_n(M=50, A=Amp):
    N=M+1
    # the first element in h_sum will be zero, because in this case we only add A[0], which is 1
    h_sum = np.zeros(26, dtype='complex_')
    z = complex(0,1)
    print(z)
    h_array = np.zeros(26)
    for i in range(len(h_array)):         # compute ith element of h
        

        # if we vary the range of the loop we get completely different stuff
        for j in range(1,26):
            h_sum[i] += A[j]*np.exp(-z*np.pi*j*((M-2*i)/N))   # hier war vorher das j im exp nicht da 
    
    

    for i in range(len(h_array)):
        h_array[i] = (1/(N) * (A[0] + 2* h_sum[i]))
    print(h_array)
    return h_array



# Apply the impulse response to your generated noise.
def apply_to_noise():
    h = h_of_n()
    return np.convolve(h, signal)
    # new_array = np.zeros(len(noise))
    # for i in range(len(h)):
    #     if 
    #     new_array[i] = 
    # return new_array

# transform into frequency domain
# A_back = np.fft.rfft(Amp)


convolution = apply_to_noise()

# convolution = convolution[::4]

convolution_f = np.fft.rfft(convolution)

convolution_f = convolution_f[::4]
print(np.shape(convolution), np.shape(convolution_f))
plt.figure()
plt.plot(convolution_f)
plt.title('Frequency spectrum of the filtered noise')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.show()