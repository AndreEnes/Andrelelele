import numpy as np
from sklearn.preprocessing import RobustScaler

class Player:
    """Class gathers all information needed to generate the audio sample"""
    def __init__(self, sample_duration=1, sample_frequency=5000, sample_rate=44100, samples_per_wave=100, scaler="MinMax", debug_mode=False):
        self.sample_duration = sample_duration
        self.sample_frequency = sample_frequency
        self.sample_rate = sample_rate
        self.samples_per_wave = samples_per_wave
        self.scaler = scaler
        self.debug_mode = debug_mode
        self.debug_x = []

    def generate_waveform(self, points):
        """Generate the drawing waveform"""
        # Doodle points can overlap, but overlap is not a valid function
        self._remove_overlap(points)

        # Resample the drawn points
        x_new, y_new = self._resample_points(points["x"], points["y"])

        # Calculate how many cycles needed for 1 second of audio
        num_cycles = self._calculate_cycles_for_duration(self.samples_per_wave, self.sample_duration, self.sample_rate)
        
        # Create periodic waveform with alternating cycles
        self.debug_x, waveform_y = self._create_periodic_waveform(x_new, y_new, num_cycles)

        # Normalize audio data
        audio_data = self._normalize_audio(waveform_y)
        
        return audio_data
    
    def debug_waveform(self):
        """Get the x axis of the generated audio data"""
        return self.debug_x, self.samples_per_wave
    
    def _interpolate(self, x, x0, y0, x1, y1):
        """Linear interpolation between two points."""
        if x1 == x0:
            return y0
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

    def _find_closest_points(self, x, x_values, y_values):
        """Find the two closest points for interpolation."""
        diffs = np.abs(np.array(x_values) - x)
        indices = np.argsort(diffs)[:2]

        i1, i2 = indices[0], indices[1]
        return x_values[i1], y_values[i1], x_values[i2], y_values[i2]
    
    def _remove_overlap(self, points):
        """Remove doodle overlap to turn the points into a valid function"""
        return
    
    def _resample_points(self, x_values, y_values):
        """Resample points using linear interpolation."""
        samples_per_half_wave = self.samples_per_wave / 2

        x_max = max(x_values)
        x_new = np.linspace(0, x_max, int(samples_per_half_wave))
        y_new = []

        for x in x_new:
            x0, y0, x1, y1 = self._find_closest_points(x, x_values, y_values)
            y_new.append(self._interpolate(x, x0, y0, x1, y1))

        return x_new, y_new
    
    def _calculate_cycles_for_duration(self, cycle_length, seconds, sample_rate=44100):
        """Calculate how many cycles needed for a given duration."""
        # TODO fix
        
        total_samples = sample_rate * seconds
        
        return int(total_samples / cycle_length)
    
    def _create_periodic_waveform(self, x_values, y_values, num_cycles):
        """Create a periodic waveform by repeating and alternating the pattern."""
        x_cycle = max(x_values)
        waveform_x = []
        waveform_y = []

        for cycle in range(num_cycles):
            offset = cycle * x_cycle

            for i, (x, y) in enumerate(zip(x_values, y_values)):
                new_x = x + offset
                # Alternate sign every other cycle
                new_y = y if cycle % 2 == 0 else -y

                waveform_x.append(new_x)
                waveform_y.append(new_y)

        return np.array(waveform_x), np.array(waveform_y)
    
    # TODO Select scaler based on output volume
    def _normalize_audio(self, points):
        """Normalize audio data to [-1, 1] range."""
        if len(points) == 0:
            return points

        if self.scaler == "MinMax":
            return self._minMax_scaler(points)
        elif self.scaler == "Robust":
            return self._robust_scaler(points)
    
    def _minMax_scaler(self, X):
        if len(X) == 0:
            return X

        # X is the variable, not the x axis
        X_min = np.min(X)
        X_max = np.max(X)

        # Min-max scaling adjusted to [-1, 1]
        return 2 * (X - X_min) / (X_max - X_min) - 1

    def _robust_scaler(self, X):
        if len(X) == 0:
            return X
        
        # Reshape to 2D array for sklearn (column vector)
        X_reshaped = np.array(X).reshape(-1, 1)
        transformer = RobustScaler().fit(X_reshaped)
        # Transform and flatten back to 1D
        X_output = transformer.transform(X_reshaped).flatten()

        return np.clip(X_output, -1, 1)
