library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tt_um_arsik is
    port (     
        ui_in   : in  std_logic_vector(7 downto 0);     -- Operator
        uo_out  : out std_logic_vector(7 downto 0);     -- Result
        uio_in  : in  std_logic_vector(7 downto 0);
        uio_out : out std_logic_vector(7 downto 0);
        uio_oe  : out std_logic_vector(7 downto 0);
        ena     : in  std_logic;
        clk     : in  std_logic;
        rst_n   : in  std_logic
    );
end tt_um_arsik;

architecture Behavioral of tt_um_arsik is
    type state_t is (IDLE, ADDITION, SUBTRACTION, WAIT_RELEASE, DIVIDE);
    signal state : state_t;

    signal inp : unsigned(5 downto 0); 
    signal operator : unsigned(1 downto 0);

    signal res : unsigned(7 downto 0) := (others => '0');

    signal div_count : unsigned(7 downto 0) := (others => '0');
    signal div_rest : unsigned(7 downto 0) := (others => '0');
begin

    process (clk)
    begin
        if rising_edge(clk) then
            inp <= unsigned(ui_in(5 downto 0));
            operator <= unsigned(ui_in(7 downto 6));
        end if;
    end process;

    process (clk, rst_n)
    begin
        if rst_n = '0' then
            state <= IDLE;
            res <= (others => '0');

        elsif rising_edge(clk) then
            case state is
                when IDLE =>
                    if operator = "00" then
                        state <= IDLE;
                    elsif operator = "01" then
                        state <= ADDITION;
                    elsif operator = "10" then
                        state <= SUBTRACTION;
                    else
                        div_rest <= res;
                        state <= DIVIDE;
                    end if;
                
                when ADDITION =>
                    res <= res + resize(inp, 8);
                    state <= WAIT_RELEASE;

                when SUBTRACTION =>
                    res <= res - resize(inp, 8);
                    state <= WAIT_RELEASE;
                
                when DIVIDE =>
                    if inp = 0 then
                        state <= WAIT_RELEASE;
                    elsif div_rest >= resize(inp, 8) then
                        div_rest <= div_rest - resize(inp, 8);
                        div_count <= div_count + 1;
                        state <= DIVIDE;
                    else
                        res <= div_count;
                        div_count <= (others => '0');
                        div_rest <= (others => '0');
                        state <= WAIT_RELEASE;
                    end if;

                when WAIT_RELEASE =>
                    if operator = "00" then
                        state <= IDLE;
                    else 
                        state <= WAIT_RELEASE;
                    end if;
                
            end case;
        end if;
    end process;        

    uo_out <= std_logic_vector(res);
    uio_out <= "00000000";
    uio_oe <= "00000000";
end Behavioral;