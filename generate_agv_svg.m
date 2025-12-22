function generate_agv_svg()
    % Ensure directory exists
    if ~exist('results/papers', 'dir')
        mkdir('results/papers');
    end

    filename = 'results/papers/agv_model.svg';
    fid = fopen(filename, 'w');
    
    if fid == -1
        error('Cannot open file %s', filename);
    end

    % Parameters
    L = 200;  % Scale: 1m = 100px
    W = 80;
    WheelW = 20;
    WheelL = 40;
    
    % Canvas
    CanvasW = 800;
    CanvasH = 600;
    
    % Origin (Bottom Left)
    Ox = 50; Oy = 550;
    
    % Vehicle Center (Global) - Place it to allow drawing R vectors
    Cx = 500; Cy = 300; 
    
    % Heading (Up)
    psi = -pi/2; % Pointing UP in SVG coords (Y is down)
    
    % ICR (Left side)
    R_turn = 300; % 3m radius
    ICRx = Cx - R_turn; 
    ICRy = Cy;
    
    % Vehicle Corners (Body Frame, Centered at Cx, Cy)
    % Body Frame: x forward (Up), y left (Left)
    % Global Frame: X right, Y down
    % Transform Body(bx, by) to Global(gx, gy):
    % gx = Cx + bx*cos(psi) - by*sin(psi)
    % gy = Cy + bx*sin(psi) + by*cos(psi)
    
    % Function to transform points
    function [gx, gy] = trans(bx, by, cx, cy, head)
        gx = cx + bx*cos(head) - by*sin(head);
        gy = cy + bx*sin(head) + by*cos(head);
    end

    % SVG Header
    fprintf(fid, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n');
    fprintf(fid, '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" version="1.1">\n', CanvasW, CanvasH);
    fprintf(fid, '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="black" /></marker></defs>\n');
    
    % 1. Global Axes
    fprintf(fid, '<g stroke="black" stroke-width="2" marker-end="url(#arrow)">\n');
    fprintf(fid, '<line x1="%d" y1="%d" x2="%d" y2="%d" />\n', Ox, Oy, Ox+100, Oy); % X axis
    fprintf(fid, '<line x1="%d" y1="%d" x2="%d" y2="%d" />\n', Ox, Oy, Ox, Oy-100); % Y axis
    fprintf(fid, '</g>\n');
    fprintf(fid, '<text x="%d" y="%d" font-family="Arial" font-size="20">O</text>\n', Ox-20, Oy+20);
    fprintf(fid, '<text x="%d" y="%d" font-family="Arial" font-size="20">X</text>\n', Ox+110, Oy+5);
    fprintf(fid, '<text x="%d" y="%d" font-family="Arial" font-size="20">Y</text>\n', Ox-5, Oy-110);

    % 2. Vehicle Body (Rectangle)
    % Corners in Body Frame: [L/2, W/2], [L/2, -W/2], [-L/2, -W/2], [-L/2, W/2]
    % Note: y is Left, so W/2 is Left.
    bx = [L/2, L/2, -L/2, -L/2];
    by = [-W/2, W/2, W/2, -W/2]; % Right, Left, Left, Right
    
    gX = zeros(1,4); gY = zeros(1,4);
    for i=1:4
        [gX(i), gY(i)] = trans(bx(i), by(i), Cx, Cy, psi);
    end
    
    fprintf(fid, '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="black" stroke-width="2" />\n', ...
        gX(1), gY(1), gX(2), gY(2), gX(3), gY(3), gX(4), gY(4));

    % 3. Centerlines (Longitudinal & Lateral)
    % Longitudinal
    [lx1, ly1] = trans(L/2+20, 0, Cx, Cy, psi);
    [lx2, ly2] = trans(-L/2-20, 0, Cx, Cy, psi);
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="1" stroke-dasharray="5,5" />\n', lx1, ly1, lx2, ly2);
    
    % Lateral (Rear Axle? No, Center)
    [wx1, wy1] = trans(0, W/2+20, Cx, Cy, psi);
    [wx2, wy2] = trans(0, -W/2-20, Cx, Cy, psi);
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="1" stroke-dasharray="5,5" />\n', wx1, wy1, wx2, wy2);

    % 4. Wheels
    % Positions in Body Frame: LF(L/2, W/2), RF(L/2, -W/2), LR(-L/2, W/2), RR(-L/2, -W/2)
    % Wait, parameters.m Lf=Lr=1.0, total L=2.0. So axles are at +/- L/2.
    % Wheel names: 
    % LF (Left Front): x=L/2, y=W/2 (Body: y is left)
    % RF (Right Front): x=L/2, y=-W/2
    % LR (Left Rear): x=-L/2, y=W/2
    % RR (Right Rear): x=-L/2, y=-W/2
    
    w_pos_x = [L/2, L/2, -L/2, -L/2];
    w_pos_y = [W/2, -W/2, W/2, -W/2]; % LF, RF, LR, RR
    
    % Calculate Steering Angles (Ackermann / ICR)
    % Vector from Wheel to ICR must be perpendicular to wheel direction
    % ICR in Body Frame:
    % cx_b = (ICRx - Cx)*cos(-psi) - (ICRy - Cy)*sin(-psi)
    % cy_b = (ICRx - Cx)*sin(-psi) + (ICRy - Cy)*cos(-psi)
    % Wait, simplier: ICR is at Body (0, R_turn) (y is Left, so positive R_turn)
    icr_bx = 0; icr_by = R_turn; 
    
    for i=1:4
        % Vector from Wheel to ICR
        dx = icr_bx - w_pos_x(i);
        dy = icr_by - w_pos_y(i);
        % Angle of radius line
        ang_rad = atan2(dy, dx);
        % Wheel angle = ang_rad - pi/2
        delta = ang_rad - pi/2;
        
        % For RF and LR (Passive), they follow motion? 
        % Diagonal Steering: LF and RR are steered. 
        % RF and LR are castors? Or fixed? 
        % Usually "Double Steer" implies 2 steered. Assume others are castors aligning with flow.
        % So draw all with correct angle.
        
        [wcx, wcy] = trans(w_pos_x(i), w_pos_y(i), Cx, Cy, psi);
        
        % Draw Wheel Rect
        % Wheel Local Frame: x_w aligned with wheel Direction
        % Transform corner points
        w_angle = psi + delta;
        
        wx = [WheelL/2, WheelL/2, -WheelL/2, -WheelL/2];
        wy = [-WheelW/2, WheelW/2, WheelW/2, -WheelW/2];
        
        poly_pts = '';
        for k=1:4
             p_gx = wcx + wx(k)*cos(w_angle) - wy(k)*sin(w_angle);
             p_gy = wcy + wx(k)*sin(w_angle) + wy(k)*cos(w_angle);
             poly_pts = [poly_pts, sprintf('%.1f,%.1f ', p_gx, p_gy)];
        end
        
        % Style: Active (LF 1, RR 4) darker?
        if i==1 || i==4
             fillcolor = '#D0D0D0'; stroke_w = 2;
        else
             fillcolor = 'white'; stroke_w = 1; % Passive
        end
        fprintf(fid, '<polygon points="%s" fill="%s" stroke="black" stroke-width="%d" />\n', poly_pts, fillcolor, stroke_w);
        
        % Radius Line (from ICR to Wheel Center)
        fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="gray" stroke-width="0.5" />\n', ICRx, ICRy, wcx, wcy);
    end
    
    % 5. ICR Point
    fprintf(fid, '<circle cx="%.1f" cy="%.1f" r="3" fill="black" />\n', ICRx, ICRy);
    fprintf(fid, '<text x="%.1f" y="%.1f" font-family="Arial" font-size="16">C</text>\n', ICRx-20, ICRy);
    
    % Center Radius Line
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="1" />\n', ICRx, ICRy, Cx, Cy);
    fprintf(fid, '<text x="%.1f" y="%.1f" font-family="Arial" font-size="16">R</text>\n', (ICRx+Cx)/2, Cy-10);

    % 6. Velocity Vector at CG
    v_len = 60;
    % beta is side slip. 
    beta = 0; % Simplified
    vx_end = Cx + v_len*cos(psi+beta);
    vy_end = Cy + v_len*sin(psi+beta);
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="2" marker-end="url(#arrow)" />\n', Cx, Cy, vx_end, vy_end);
    fprintf(fid, '<text x="%.1f" y="%.1f" font-family="Arial" font-size="16">v</text>\n', vx_end+10, vy_end);

    % 7. Labels
    % Wheelbase L
    dim_off = W/2 + 60;
    [d1x, d1y] = trans(L/2, -dim_off, Cx, Cy, psi);
    [d2x, d2y] = trans(-L/2, -dim_off, Cx, Cy, psi);
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="1" />\n', d1x, d1y, d2x, d2y);
    % Extension lines
    [e1x, e1y] = trans(L/2, -W/2, Cx, Cy, psi);
    [e2x, e2y] = trans(-L/2, -W/2, Cx, Cy, psi);
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="0.5" />\n', e1x, e1y, d1x, d1y);
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="0.5" />\n', e2x, e2y, d2x, d2y);
    fprintf(fid, '<text x="%.1f" y="%.1f" font-family="Arial" font-size="16">L</text>\n', (d1x+d2x)/2 + 10, (d1y+d2y)/2);

    % Track Width W
    dim_off_w = L/2 + 40;
    [w1x, w1y] = trans(dim_off_w, W/2, Cx, Cy, psi);
    [w2x, w2y] = trans(dim_off_w, -W/2, Cx, Cy, psi);
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="1" />\n', w1x, w1y, w2x, w2y);
    % Extension lines
    [ew1x, ew1y] = trans(L/2, W/2, Cx, Cy, psi);
    [ew2x, ew2y] = trans(L/2, -W/2, Cx, Cy, psi);
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="0.5" />\n', ew1x, ew1y, w1x, w1y);
    fprintf(fid, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="black" stroke-width="0.5" />\n', ew2x, ew2y, w2x, w2y);
    fprintf(fid, '<text x="%.1f" y="%.1f" font-family="Arial" font-size="16">W</text>\n', (w1x+w2x)/2, (w1y+w2y)/2 - 10);

    % Labels: delta_lf, delta_rr
    % Just simple text near wheels
    [tlx, tly] = trans(L/2, W/2+30, Cx, Cy, psi);
    fprintf(fid, '<text x="%.1f" y="%.1f" font-family="Arial" font-size="14">δ_lf</text>\n', tlx, tly);
    [trx, try] = trans(-L/2, -W/2-30, Cx, Cy, psi);
    fprintf(fid, '<text x="%.1f" y="%.1f" font-family="Arial" font-size="14">δ_rr</text>\n', trx, try);

    fprintf(fid, '</svg>\n');
    fclose(fid);
    fprintf('SVG generated at %s\n', filename);
end
