function [q] = catmull_rom_t(control_x, control_y, T)
  q = @(t) 1/2*[t^3 t^2 t 1]*[-1/T (4*T-1)/T (-4*T +1)/T 1/T; 2/T (-6*T+1)/T (6*T-2)/T -1/T; -1/T 0 1/T 0; 0 2 0 0]*[control_x' control_y'];
end
