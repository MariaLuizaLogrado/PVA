clear all
clc
close all

%control_x = [1 2 3 5 7 4 1 2 3 5];
%control_y = [2 4 6 7 1 1 2 4 6 7];

control_x = [3 4 6 7 6 4 3 4 6 7];
control_y = [5 6 6 5 4 4 5 6 6 5];
T = 1;
t = 0:0.01:1;
N = numel(control_x);

interpolated_points = zeros(numel(t), 2);
X = zeros(numel(t), N-3);
Y = zeros(numel(t), N-3);

for i = 1:N-3
   vx(i,:) = control_x(i:i+3);
   vy(i,:) = control_y(i:i+3);
endfor

S = size(vx);

% for i = 1:S(1)
%   vx1 = vx(i,:);
%   vy1 = vy(i,:);
%   q_aux = catmull_rom_t(vx1, vy1, T);
%   for j = 1:numel(t)
%      interpolated_points(j,:) = q_aux(t(j));
%   endfor
%   X(:,i) = interpolated_points(:,1);
%   Y(:,i) = interpolated_points(:,2);
% endfor

% plot(control_x, control_y, '*k', 'linewidth', 2);
% hold on
% grid on
% for i = 1:N-3
%   plot(X(:,i), Y(:,i), '-b', 'linewidth', 1);
%   legend({'Pontos de controle', 'Spline'}, 'location', 'southwest')
%   title(['T = ', num2str(T)])
%   xlabel('x','fontsize',15)
%   ylabel('y','fontsize',15)
%   xlim([0 10])
%   ylim([0 8])
%   pause(0.05)
% end
% figure (1,"PaperUnits", 'centimeters',...
% "PaperSize",[15 10], "PaperPosition",[0 0 15 10])

% % Save the figure with a unique filename for each iteration
% print(['cat_rom_t1'],'-dpng','-r600')


% %{
% filename = 'cat_rom_t025.gif';
% DelayTime = 0;
% f = figure;

% for i = 1:N-3
%   plot(control_x, control_y, '*k', 'linewidth', 2);
%   hold on
%   grid on
%   plot(X(:,i), Y(:,i), '-b', 'linewidth', 1);
%   title(['T = ', num2str(T)])
%   legend({'Pontos de controle', 'Spline'}, 'location', 'northwest')
%   xlim([0 10])
%   ylim([0 8])
%   pause(1)
%   frame = getframe(f);
%   im = frame2im(frame);
%   [imind,cm] = rgb2ind(im);

%   imwrite(imind,cm,filename,'gif','WriteMode','append','DelayTime', DelayTime , 'Compression' , 'lzw');
% end


