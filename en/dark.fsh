#ifdef GL_ES
precision mediump float;
#endif
varying vec4 v_fragmentColor;
varying vec2 v_texCoord;

void main(void)
{
    gl_FragColor = v_fragmentColor*texture2D(CC_Texture0, v_texCoord);
    gl_FragColor.rgb *= 0.5;
}