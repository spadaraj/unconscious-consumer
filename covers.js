// ===== GENERATIVE SVG COVER SYSTEM =====
// Each category gets a unique procedural cover visual.
// generateCover(category, animated) returns an HTML string.
// animated=false → static SVG (homepage cards, 180px)
// animated=true  → SVG + <script> block (article page, 280px)

var COVER_BG = '#1A0E0A';
var COVER_ACCENT = '#C4531A';
var COVER_CREAM = '#F5F0E8';

// ===== DISPATCHER =====
function generateCover(category, animated) {
  var h = animated ? 280 : 180;
  switch (category) {
    case 'consumer-psychology':   return coverConsumerPsychology(h, animated);
    case 'behavioural-economics': return coverBehaviouralEconomics(h, animated);
    case 'user-experience':       return coverUserExperience(h, animated);
    case 'undercurrents':         return coverUndercurrents(h, animated);
    default:                      return coverConsumerPsychology(h, animated);
  }
}

// ===== COVER 1: CONSUMER PSYCHOLOGY =====
// Dual reality — blurred left vs sharp right, divided by oscillating line
function coverConsumerPsychology(h, animated) {
  var mid = 330;
  var cy = Math.round(h * 0.5);

  // Shared geometry offsets
  var nodes = [
    { x: -85, y: -30, r: 4 },
    { x: 55,  y: 40,  r: 3 },
    { x: -35, y: 60,  r: 5 },
    { x: 35,  y: -40, r: 3 }
  ];

  function drawGroup(cx, baseOpacity, filtered) {
    var g = '';
    // Concentric circles
    [25, 45, 65].forEach(function(r, i) {
      var op = baseOpacity + i * 0.15;
      g += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="none" stroke="' + COVER_ACCENT + '" stroke-width="1" opacity="' + op.toFixed(2) + '"/>';
    });
    // Scattered nodes
    nodes.forEach(function(n) {
      g += '<circle cx="' + (cx + n.x) + '" cy="' + (cy + n.y) + '" r="' + n.r + '" fill="' + COVER_ACCENT + '" opacity="' + (baseOpacity * 0.8).toFixed(2) + '"/>';
    });
    // Connecting lines
    g += '<line x1="' + (cx + nodes[0].x) + '" y1="' + (cy + nodes[0].y) + '" x2="' + (cx + nodes[2].x) + '" y2="' + (cy + nodes[2].y) + '" stroke="' + COVER_CREAM + '" stroke-width="0.5" opacity="0.15"/>';
    g += '<line x1="' + (cx + nodes[1].x) + '" y1="' + (cy + nodes[1].y) + '" x2="' + (cx + nodes[3].x) + '" y2="' + (cy + nodes[3].y) + '" stroke="' + COVER_CREAM + '" stroke-width="0.5" opacity="0.15"/>';
    return g;
  }

  var animStyle = '';
  var lineClass = '';
  if (animated) {
    lineClass = ' class="cp-divider"';
    animStyle = '<style>' +
      '@keyframes cpShift { 0%,100% { transform: translateX(0); } 50% { transform: translateX(-20px); } }' +
      '.cp-divider { animation: cpShift 4s ease-in-out infinite; transform-origin: 330px 0; }' +
      '.cp-left-clip rect { animation: cpShift 4s ease-in-out infinite; }' +
      '</style>';
  }

  var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 ' + h + '" preserveAspectRatio="xMidYMid slice">' +
    animStyle +
    '<defs>' +
    '<clipPath id="cp-left" class="cp-left-clip"><rect x="0" y="0" width="' + mid + '" height="' + h + '"/></clipPath>' +
    '<clipPath id="cp-right"><rect x="' + mid + '" y="0" width="' + mid + '" height="' + h + '"/></clipPath>' +
    '<filter id="cp-blur"><feGaussianBlur stdDeviation="4"/></filter>' +
    '</defs>' +
    '<rect width="660" height="' + h + '" fill="' + COVER_BG + '"/>' +
    // Left group — blurred
    '<g clip-path="url(#cp-left)" filter="url(#cp-blur)">' + drawGroup(165, 0.5, true) + '</g>' +
    // Right group — sharp
    '<g clip-path="url(#cp-right)">' + drawGroup(495, 0.7, false) + '</g>' +
    // Divider
    '<line' + lineClass + ' x1="' + mid + '" y1="0" x2="' + mid + '" y2="' + h + '" stroke="' + COVER_ACCENT + '" stroke-width="1" opacity="0.7"/>' +
    // Labels
    '<text x="165" y="16" text-anchor="middle" fill="' + COVER_CREAM + '" font-family="Inter,sans-serif" font-size="8" letter-spacing="0.1em" opacity="0.35">PERCEIVED</text>' +
    '<text x="495" y="16" text-anchor="middle" fill="' + COVER_CREAM + '" font-family="Inter,sans-serif" font-size="8" letter-spacing="0.1em" opacity="0.35">ACTUAL</text>' +
    '</svg>';

  return svg;
}

// ===== COVER 2: BEHAVIOURAL ECONOMICS =====
// Flow field — sinusoidal curves with drifting particles
function coverBehaviouralEconomics(h, animated) {
  // Seeded pseudo-random for consistent particle placement
  var seed = 42;
  function rand() {
    seed = (seed * 16807 + 0) % 2147483647;
    return (seed - 1) / 2147483646;
  }

  var numPaths = 5;
  var numParticles = 20;

  // Generate flow paths as sine-based curves
  var paths = [];
  for (var p = 0; p < numPaths; p++) {
    var baseY = (h / (numPaths + 1)) * (p + 1);
    var amp = 12 + rand() * 16;
    var freq = 0.008 + rand() * 0.006;
    var phase = rand() * Math.PI * 2;
    paths.push({ baseY: baseY, amp: amp, freq: freq, phase: phase });
  }

  // Build path d strings
  function pathY(p, x) {
    return p.baseY + Math.sin(x * p.freq + p.phase) * p.amp;
  }

  var pathStrings = [];
  for (var p = 0; p < numPaths; p++) {
    var d = 'M 0 ' + pathY(paths[p], 0).toFixed(1);
    for (var x = 10; x <= 660; x += 10) {
      d += ' L ' + x + ' ' + pathY(paths[p], x).toFixed(1);
    }
    pathStrings.push(d);
  }

  // Generate particles
  var particles = [];
  for (var i = 0; i < numParticles; i++) {
    var pIdx = Math.floor(rand() * numPaths);
    var startX = rand() * 660;
    var startY = pathY(paths[pIdx], startX);
    var isTerracotta = rand() < 0.3;
    var opacity = 0.5 + rand() * 0.3;
    var speed = 0.3 + rand() * 0.4;
    particles.push({
      pathIdx: pIdx, x: startX, y: startY,
      color: isTerracotta ? COVER_ACCENT : COVER_CREAM,
      opacity: opacity, speed: speed, id: 'be-p-' + i
    });
  }

  var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 ' + h + '" preserveAspectRatio="xMidYMid slice">' +
    '<rect width="660" height="' + h + '" fill="' + COVER_BG + '"/>';

  // Draw flow paths
  for (var p = 0; p < numPaths; p++) {
    svg += '<path d="' + pathStrings[p] + '" fill="none" stroke="' + COVER_CREAM + '" stroke-width="0.6" opacity="0.2"/>';
  }

  // Draw particles
  for (var i = 0; i < particles.length; i++) {
    var pt = particles[i];
    svg += '<circle id="' + pt.id + '" cx="' + pt.x.toFixed(1) + '" cy="' + pt.y.toFixed(1) + '" r="2.5" fill="' + pt.color + '" opacity="' + pt.opacity.toFixed(2) + '"/>';
  }

  svg += '</svg>';

  if (animated) {
    // Serialize path data for the animation script
    var pathData = JSON.stringify(paths.map(function(p) {
      return { baseY: p.baseY, amp: p.amp, freq: p.freq, phase: p.phase };
    }));
    var particleData = JSON.stringify(particles.map(function(pt) {
      return { pathIdx: pt.pathIdx, x: pt.x, speed: pt.speed, id: pt.id };
    }));

    svg += '<script>' +
      '(function(){' +
      'var bePaths=' + pathData + ';' +
      'var beParticles=' + particleData + ';' +
      'function bePathY(p,x){return p.baseY+Math.sin(x*p.freq+p.phase)*p.amp;}' +
      'function beAnimate(){' +
        'for(var i=0;i<beParticles.length;i++){' +
          'var pt=beParticles[i];' +
          'pt.x+=pt.speed;' +
          'if(pt.x>660)pt.x=0;' +
          'var y=bePathY(bePaths[pt.pathIdx],pt.x);' +
          'var el=document.getElementById(pt.id);' +
          'if(el){el.setAttribute("cx",pt.x.toFixed(1));el.setAttribute("cy",y.toFixed(1));}' +
        '}' +
        'requestAnimationFrame(beAnimate);' +
      '}' +
      'requestAnimationFrame(beAnimate);' +
      '})();' +
      '<\/script>';
  }

  return svg;
}

// ===== COVER 3: USER EXPERIENCE =====
// Path map — grid, primary path, dashed dead-end secondaries
function coverUserExperience(h, animated) {
  var gridSpacingX = 110;
  var gridSpacingY = h >= 280 ? 70 : 68;

  // Key coordinates
  var startPt   = { x: 80,  y: 30 };
  var corner1   = { x: 80,  y: Math.round(h * 0.55) };
  var corner2   = { x: 330, y: Math.round(h * 0.55) };
  var endPt     = { x: 580, y: Math.round(h * 0.85) };
  var deadEndPt = { x: 400, y: Math.round(h * 0.7) };
  var secBEnd   = { x: 570, y: Math.round(h * 0.2) };

  // Grid
  var gridLines = '';
  for (var gx = gridSpacingX; gx < 660; gx += gridSpacingX) {
    gridLines += '<line x1="' + gx + '" y1="0" x2="' + gx + '" y2="' + h + '" stroke="' + COVER_CREAM + '" stroke-width="0.5" opacity="0.1"/>';
  }
  for (var gy = gridSpacingY; gy < h; gy += gridSpacingY) {
    gridLines += '<line x1="0" y1="' + gy + '" x2="660" y2="' + gy + '" stroke="' + COVER_CREAM + '" stroke-width="0.5" opacity="0.1"/>';
  }

  // Primary path
  var primaryD = 'M ' + startPt.x + ' ' + startPt.y +
    ' L ' + corner1.x + ' ' + corner1.y +
    ' L ' + corner2.x + ' ' + corner2.y +
    ' L ' + endPt.x + ' ' + endPt.y;

  // Secondary paths
  var secAD = 'M ' + startPt.x + ' ' + startPt.y + ' L 400 30 L ' + deadEndPt.x + ' ' + deadEndPt.y;
  var secBD = 'M ' + corner2.x + ' ' + corner2.y + ' L ' + secBEnd.x + ' ' + secBEnd.y;

  // Traveler (animated only)
  var travelerSvg = '';
  if (animated) {
    travelerSvg = '<circle id="ux-traveler" cx="' + startPt.x + '" cy="' + startPt.y + '" r="3" fill="' + COVER_ACCENT + '" opacity="1"/>';
  }

  var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 ' + h + '" preserveAspectRatio="xMidYMid slice">' +
    '<rect width="660" height="' + h + '" fill="' + COVER_BG + '"/>' +
    // Grid
    gridLines +
    // Secondary path A (dashed, dead end)
    '<path d="' + secAD + '" fill="none" stroke="' + COVER_CREAM + '" stroke-width="0.8" stroke-dasharray="4 5" opacity="0.25"/>' +
    // Dead end rect
    '<rect x="' + (deadEndPt.x - 10) + '" y="' + (deadEndPt.y - 6) + '" width="20" height="12" rx="2" fill="none" stroke="' + COVER_CREAM + '" stroke-width="0.8" opacity="0.2"/>' +
    // Secondary path B (dashed, off edge)
    '<path d="' + secBD + '" fill="none" stroke="' + COVER_CREAM + '" stroke-width="0.6" stroke-dasharray="2 6" opacity="0.15"/>' +
    // Primary path
    '<path d="' + primaryD + '" fill="none" stroke="' + COVER_ACCENT + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
    // Start and end dots
    '<circle cx="' + startPt.x + '" cy="' + startPt.y + '" r="4" fill="' + COVER_ACCENT + '"/>' +
    '<circle cx="' + endPt.x + '" cy="' + endPt.y + '" r="4" fill="' + COVER_ACCENT + '"/>' +
    // Corner dots
    '<circle cx="' + corner1.x + '" cy="' + corner1.y + '" r="2.5" fill="' + COVER_ACCENT + '" opacity="0.6"/>' +
    '<circle cx="' + corner2.x + '" cy="' + corner2.y + '" r="2.5" fill="' + COVER_ACCENT + '" opacity="0.6"/>' +
    // Labels
    '<text x="' + startPt.x + '" y="' + (startPt.y - 10) + '" text-anchor="middle" fill="' + COVER_ACCENT + '" font-family="Inter,sans-serif" font-size="7" letter-spacing="0.06em" opacity="0.6">START</text>' +
    '<text x="' + endPt.x + '" y="' + (endPt.y - 12) + '" text-anchor="middle" fill="' + COVER_ACCENT + '" font-family="Inter,sans-serif" font-size="7" letter-spacing="0.06em" opacity="0.6">END</text>' +
    '<text x="' + (deadEndPt.x + 20) + '" y="' + (deadEndPt.y + 4) + '" fill="' + COVER_CREAM + '" font-family="Inter,sans-serif" font-size="6" opacity="0.2">dead end</text>' +
    // Traveler dot
    travelerSvg +
    '</svg>';

  if (animated) {
    var waypoints = JSON.stringify([
      startPt, corner1, corner2, endPt
    ]);
    svg += '<script>' +
      '(function(){' +
      'var uxWaypoints=' + waypoints + ';' +
      'var uxSegLens=[];' +
      'var uxTotalLen=0;' +
      'for(var i=0;i<uxWaypoints.length-1;i++){' +
        'var dx=uxWaypoints[i+1].x-uxWaypoints[i].x;' +
        'var dy=uxWaypoints[i+1].y-uxWaypoints[i].y;' +
        'var len=Math.sqrt(dx*dx+dy*dy);' +
        'uxSegLens.push(len);uxTotalLen+=len;' +
      '}' +
      'var uxDuration=5000;' +
      'var uxPauseTime=300;' +
      'var uxStart=performance.now();' +
      'var uxTraveler=document.getElementById("ux-traveler");' +
      'function uxAnimate(now){' +
        'if(!uxTraveler){uxTraveler=document.getElementById("ux-traveler");}' +
        'if(!uxTraveler){requestAnimationFrame(uxAnimate);return;}' +
        'var elapsed=(now-uxStart)%(uxDuration+uxPauseTime*(uxWaypoints.length-2));' +
        'var dist=0;var timeAcc=0;' +
        'var pos={x:uxWaypoints[0].x,y:uxWaypoints[0].y};' +
        'var segTimeTotal=uxDuration;' +
        'for(var i=0;i<uxSegLens.length;i++){' +
          'var segFrac=uxSegLens[i]/uxTotalLen;' +
          'var segTime=segFrac*segTimeTotal;' +
          'var pauseBefore=(i>0)?uxPauseTime:0;' +
          'if(elapsed<timeAcc+pauseBefore){' +
            'pos=uxWaypoints[i];break;' +
          '}' +
          'timeAcc+=pauseBefore;' +
          'if(elapsed<timeAcc+segTime){' +
            'var t=(elapsed-timeAcc)/segTime;' +
            'pos={x:uxWaypoints[i].x+(uxWaypoints[i+1].x-uxWaypoints[i].x)*t,' +
                 'y:uxWaypoints[i].y+(uxWaypoints[i+1].y-uxWaypoints[i].y)*t};' +
            'break;' +
          '}' +
          'timeAcc+=segTime;' +
          'pos=uxWaypoints[i+1];' +
        '}' +
        'var fadeZone=uxDuration*0.05;' +
        'var totalCycle=uxDuration+uxPauseTime*(uxWaypoints.length-2);' +
        'var opacity=1;' +
        'if(elapsed>totalCycle-fadeZone)opacity=1-(elapsed-(totalCycle-fadeZone))/fadeZone;' +
        'if(elapsed<fadeZone)opacity=elapsed/fadeZone;' +
        'uxTraveler.setAttribute("cx",pos.x.toFixed(1));' +
        'uxTraveler.setAttribute("cy",pos.y.toFixed(1));' +
        'uxTraveler.setAttribute("opacity",Math.max(0,opacity).toFixed(2));' +
        'requestAnimationFrame(uxAnimate);' +
      '}' +
      'requestAnimationFrame(uxAnimate);' +
      '})();' +
      '<\/script>';
  }

  return svg;
}

// ===== COVER 4: UNDERCURRENTS =====
// Scattered dots converging into clusters — trends from noise
function coverUndercurrents(h, animated) {
  var seed = 77;
  function rand() {
    seed = (seed * 16807 + 0) % 2147483647;
    return (seed - 1) / 2147483646;
  }

  var clusters = [
    { x: 140, y: Math.round(h * 0.35) },
    { x: 360, y: Math.round(h * 0.45) },
    { x: 520, y: Math.round(h * 0.28) },
    { x: 240, y: Math.round(h * 0.65) }
  ];

  var numDots = 70;
  var maxY = h - 60; // avoid bottom text zone
  var dots = [];
  for (var i = 0; i < numDots; i++) {
    var clusterIdx = Math.floor(rand() * clusters.length);
    var startX = rand() * 640 + 10;
    var startY = rand() * maxY + 10;
    var r = 1.5 + rand() * 1.5;
    var isTerracotta = rand() < 0.2;
    var opacity = 0.3 + rand() * 0.4;
    // Static position = 40% lerp toward cluster
    var dispX = startX + (clusters[clusterIdx].x - startX) * 0.4;
    var dispY = startY + (clusters[clusterIdx].y - startY) * 0.4;
    dots.push({
      startX: startX, startY: startY,
      clusterIdx: clusterIdx,
      dispX: dispX, dispY: dispY,
      r: r, color: isTerracotta ? COVER_ACCENT : COVER_CREAM,
      opacity: opacity, isTerracotta: isTerracotta,
      id: 'uc-d-' + i
    });
  }

  var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 ' + h + '" preserveAspectRatio="xMidYMid slice">' +
    '<rect width="660" height="' + h + '" fill="' + COVER_BG + '"/>';

  for (var i = 0; i < dots.length; i++) {
    var d = dots[i];
    svg += '<circle id="' + d.id + '" cx="' + d.dispX.toFixed(1) + '" cy="' + d.dispY.toFixed(1) + '" r="' + d.r.toFixed(1) + '" fill="' + d.color + '" opacity="' + d.opacity.toFixed(2) + '"/>';
  }

  svg += '</svg>';

  if (animated) {
    var dotData = JSON.stringify(dots.map(function(d) {
      return {
        startX: d.startX, startY: d.startY,
        clusterIdx: d.clusterIdx,
        r: d.r, opacity: d.opacity,
        isTerracotta: d.isTerracotta,
        id: d.id
      };
    }));
    var clusterData = JSON.stringify(clusters);

    svg += '<script>' +
      '(function(){' +
      'var ucDots=' + dotData + ';' +
      'var ucClusters=' + clusterData + ';' +
      'var ucPhase=0;' +
      'function ucAnimate(){' +
        'ucPhase+=0.004;' +
        'var progress=Math.sin(ucPhase)*0.5+0.5;' +
        'for(var i=0;i<ucDots.length;i++){' +
          'var d=ucDots[i];' +
          'var c=ucClusters[d.clusterIdx];' +
          'var x=d.startX+(c.x-d.startX)*progress;' +
          'var y=d.startY+(c.y-d.startY)*progress;' +
          'var el=document.getElementById(d.id);' +
          'if(el){' +
            'el.setAttribute("cx",x.toFixed(1));' +
            'el.setAttribute("cy",y.toFixed(1));' +
            'if(d.isTerracotta){' +
              'var pulseOp=0.5+0.4*progress;' +
              'el.setAttribute("opacity",pulseOp.toFixed(2));' +
            '}' +
          '}' +
        '}' +
        'requestAnimationFrame(ucAnimate);' +
      '}' +
      'requestAnimationFrame(ucAnimate);' +
      '})();' +
      '<\/script>';
  }

  return svg;
}
