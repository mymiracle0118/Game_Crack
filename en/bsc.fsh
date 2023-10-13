#ifdef GL_ES
precision mediump float;
#endif
varying vec4 v_fragmentColor;
varying vec2 v_texCoord;

uniform vec4 bsc;

void main(void)
{
	gl_FragColor = v_fragmentColor * texture2D(CC_Texture0, v_texCoord);


	// 若rgba都为0则调整透明度时，如果图片经过预乘，对比度系数小于1时，计算后的透明像素会变为不透明像素。
	if (gl_FragColor.r > 0.0 || gl_FragColor.g > 0.0 || gl_FragColor.b > 0.0 || gl_FragColor.a > 0.0)
	{
		vec3 final_color = gl_FragColor.rgb * bsc.r;

		float gray = 0.2125 * final_color.r + 0.7154 * final_color.g + 0.0721 * final_color.b; 
		vec3 grayColor = vec3(gray, gray, gray);
		final_color = mix(grayColor, final_color, bsc.g);
		
		vec3 base_contrast = vec3(0.5, 0.5, 0.5);
		final_color = mix(base_contrast, final_color, bsc.b);

		gl_FragColor = vec4(final_color.rgb, gl_FragColor.a);
	}
	
}

