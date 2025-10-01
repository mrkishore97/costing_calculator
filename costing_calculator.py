import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Costing Calculator", layout="wide")

st.title("🧮 Interactive Costing Calculator")
st.markdown("Fill in any combination of values, and the calculator will compute the rest!")

# Initialize session state for values
if 'values' not in st.session_state:
    st.session_state.values = {
        'cost': None,
        'selling_price': None,
        'discounted_price': None,
        'profit': None,
        'loss': None,
        'profit_percent': None,
        'loss_percent': None,
        'discount': None
    }

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Input Values")
    
    cost = st.number_input("Total Cost ($)", min_value=0.0, value=None, step=0.01, 
                           help="The cost price of the item")
    
    selling_price = st.number_input("Selling Price ($)", min_value=0.0, value=None, step=0.01,
                                    help="The original selling price before discount")
    
    discounted_price = st.number_input("Discounted Price ($)", min_value=0.0, value=None, step=0.01,
                                       help="The final price after applying discount")
    
    discount = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=None, step=0.01,
                               help="Discount percentage on selling price")

with col2:
    st.subheader("📊 Profit/Loss Metrics")
    
    profit = st.number_input("Profit ($)", min_value=0.0, value=None, step=0.01,
                            help="Profit amount (discounted price - cost)")
    
    profit_percent = st.number_input("Profit Margin (%)", min_value=0.0, value=None, step=0.01,
                                     help="Profit percentage on cost")
    
    loss = st.number_input("Loss ($)", min_value=0.0, value=None, step=0.01,
                          help="Loss amount (cost - discounted price)")
    
    loss_percent = st.number_input("Loss Percentage (%)", min_value=0.0, max_value=100.0, value=None, step=0.01,
                                   help="Loss percentage on cost")

# Calculate button
if st.button("🔄 Calculate", type="primary", use_container_width=True):
    results = {}
    
    # Helper function to safely get values
    def get_val(val):
        return val if val not in [None, 0.0, ''] else None
    
    cost = get_val(cost)
    selling_price = get_val(selling_price)
    discounted_price = get_val(discounted_price)
    discount = get_val(discount)
    profit = get_val(profit)
    profit_percent = get_val(profit_percent)
    loss = get_val(loss)
    loss_percent = get_val(loss_percent)
    
    try:
        # Scenario 1: Cost, Profit%, Discount%
        if cost and profit_percent is not None and discount is not None:
            discounted_price = cost * (1 + profit_percent/100)
            selling_price = discounted_price / (1 - discount/100)
            profit = discounted_price - cost
            results = {
                'cost': cost,
                'selling_price': selling_price,
                'discounted_price': discounted_price,
                'discount': discount,
                'profit': profit,
                'profit_percent': profit_percent,
                'loss': 0,
                'loss_percent': 0
            }
        
        # Scenario 2: Cost and Discounted Price
        elif cost and discounted_price:
            if discounted_price >= cost:
                profit = discounted_price - cost
                profit_percent = (profit / cost) * 100
                loss = 0
                loss_percent = 0
            else:
                loss = cost - discounted_price
                loss_percent = (loss / cost) * 100
                profit = 0
                profit_percent = 0
            
            if selling_price:
                discount = ((selling_price - discounted_price) / selling_price) * 100
            elif discount is not None:
                selling_price = discounted_price / (1 - discount/100)
            else:
                selling_price = discounted_price
                discount = 0
            
            results = {
                'cost': cost,
                'selling_price': selling_price,
                'discounted_price': discounted_price,
                'discount': discount,
                'profit': profit,
                'profit_percent': profit_percent,
                'loss': loss,
                'loss_percent': loss_percent
            }
        
        # Scenario 3: Cost, Loss%
        elif cost and loss_percent is not None:
            loss = cost * (loss_percent / 100)
            discounted_price = cost - loss
            
            if discount is not None:
                selling_price = discounted_price / (1 - discount/100)
            else:
                selling_price = discounted_price
                discount = 0
            
            results = {
                'cost': cost,
                'selling_price': selling_price,
                'discounted_price': discounted_price,
                'discount': discount,
                'profit': 0,
                'profit_percent': 0,
                'loss': loss,
                'loss_percent': loss_percent
            }
        
        # Scenario 4: Selling Price and Discount%
        elif selling_price and discount is not None:
            discounted_price = selling_price * (1 - discount/100)
            
            if cost:
                if discounted_price >= cost:
                    profit = discounted_price - cost
                    profit_percent = (profit / cost) * 100
                    loss = 0
                    loss_percent = 0
                else:
                    loss = cost - discounted_price
                    loss_percent = (loss / cost) * 100
                    profit = 0
                    profit_percent = 0
            elif profit is not None:
                cost = discounted_price - profit
                profit_percent = (profit / cost) * 100 if cost > 0 else 0
                loss = 0
                loss_percent = 0
            elif profit_percent is not None:
                cost = discounted_price / (1 + profit_percent/100)
                profit = discounted_price - cost
                loss = 0
                loss_percent = 0
            else:
                cost = None
                profit = None
                profit_percent = None
                loss = None
                loss_percent = None
            
            results = {
                'cost': cost,
                'selling_price': selling_price,
                'discounted_price': discounted_price,
                'discount': discount,
                'profit': profit,
                'profit_percent': profit_percent,
                'loss': loss,
                'loss_percent': loss_percent
            }
        
        # Scenario 5: Cost and Selling Price (no discount)
        elif cost and selling_price:
            discounted_price = selling_price if not discounted_price else discounted_price
            
            if discounted_price >= cost:
                profit = discounted_price - cost
                profit_percent = (profit / cost) * 100
                loss = 0
                loss_percent = 0
            else:
                loss = cost - discounted_price
                loss_percent = (loss / cost) * 100
                profit = 0
                profit_percent = 0
            
            discount = ((selling_price - discounted_price) / selling_price) * 100 if selling_price > 0 else 0
            
            results = {
                'cost': cost,
                'selling_price': selling_price,
                'discounted_price': discounted_price,
                'discount': discount,
                'profit': profit,
                'profit_percent': profit_percent,
                'loss': loss,
                'loss_percent': loss_percent
            }
        
        else:
            st.error("⚠️ Please provide sufficient input values to calculate. Try combinations like:\n- Cost + Profit% + Discount%\n- Cost + Discounted Price\n- Selling Price + Discount%")
            st.stop()
        
        # Display results
        st.success("✅ Calculation Complete!")
        
        st.markdown("---")
        st.subheader("📋 Results Summary")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("💰 Total Cost", f"${results.get('cost', 0):.2f}" if results.get('cost') else "N/A")
            st.metric("🏷️ Selling Price", f"${results.get('selling_price', 0):.2f}" if results.get('selling_price') else "N/A")
            st.metric("💵 Discounted Price", f"${results.get('discounted_price', 0):.2f}" if results.get('discounted_price') else "N/A")
        
        with col_b:
            st.metric("📉 Discount", f"{results.get('discount', 0):.2f}%" if results.get('discount') is not None else "N/A")
            st.metric("📈 Profit", f"${results.get('profit', 0):.2f}", 
                     delta=f"{results.get('profit_percent', 0):.2f}%" if results.get('profit', 0) > 0 else None)
            
        with col_c:
            st.metric("📊 Profit Margin", f"{results.get('profit_percent', 0):.2f}%" if results.get('profit_percent') is not None else "N/A")
            if results.get('loss', 0) > 0:
                st.metric("📉 Loss", f"${results.get('loss', 0):.2f}", 
                         delta=f"-{results.get('loss_percent', 0):.2f}%", delta_color="inverse")
            else:
                st.metric("📉 Loss", "$0.00")
        
        # Detailed breakdown
        st.markdown("---")
        st.subheader("🔍 Detailed Breakdown")
        
        df = pd.DataFrame([{
            'Metric': k.replace('_', ' ').title(),
            'Value': f"${v:.2f}" if k in ['cost', 'selling_price', 'discounted_price', 'profit', 'loss'] and v is not None 
                     else f"{v:.2f}%" if v is not None else "N/A"
        } for k, v in results.items()])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Profit Margin vs Cost Variation Chart
        st.markdown("---")
        st.subheader("📊 Profit Margin vs Cost Variation")
        
        if results.get('discounted_price') and results.get('cost'):
            base_cost = results['cost']
            fixed_discounted_price = results['discounted_price']
            
            # Generate cost variations (±50% of base cost)
            cost_range = [base_cost * (0.5 + i * 0.05) for i in range(21)]
            profit_margins = []
            profits = []
            
            for cost_var in cost_range:
                if cost_var > 0:
                    profit_var = fixed_discounted_price - cost_var
                    profit_margin_var = (profit_var / cost_var) * 100
                    profit_margins.append(profit_margin_var)
                    profits.append(profit_var)
                else:
                    profit_margins.append(0)
                    profits.append(0)
            
            # Create the plot
            fig = go.Figure()
            
            # Add profit margin line
            fig.add_trace(go.Scatter(
                x=cost_range,
                y=profit_margins,
                mode='lines+markers',
                name='Profit Margin %',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=6),
                hovertemplate='Cost: $%{x:.2f}<br>Profit Margin: %{y:.2f}%<extra></extra>'
            ))
            
            # Highlight the current point
            fig.add_trace(go.Scatter(
                x=[base_cost],
                y=[results.get('profit_percent', 0)],
                mode='markers',
                name='Current Values',
                marker=dict(size=15, color='red', symbol='star'),
                hovertemplate='Current Cost: $%{x:.2f}<br>Current Profit Margin: %{y:.2f}%<extra></extra>'
            ))
            
            # Add zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Update layout
            fig.update_layout(
                title=f"How Profit Margin Changes with Cost (Fixed Discounted Price: ${fixed_discounted_price:.2f})",
                xaxis_title="Cost ($)",
                yaxis_title="Profit Margin (%)",
                hovermode='closest',
                showlegend=True,
                height=400,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add explanation
            st.info(f"📌 This chart shows how profit margin varies with cost when the discounted price is fixed at ${fixed_discounted_price:.2f}. Lower costs lead to higher profit margins!")
        
    except Exception as e:
        st.error(f"❌ Calculation error: {str(e)}")
        st.info("Please check your input values and try again.")

# Add helpful information
with st.expander("ℹ️ How to Use This Calculator"):
    st.markdown("""
    **This calculator supports various scenarios:**
    
    1. **Cost + Profit% + Discount%**: Calculate selling and discounted prices
    2. **Cost + Discounted Price**: Calculate profit/loss margins
    3. **Cost + Loss%**: Calculate the discounted price after loss
    4. **Selling Price + Discount%**: Calculate discounted price (add cost for profit/loss)
    5. **Cost + Selling Price**: Calculate profit and discount
    
    **Key Formulas:**
    - Profit = Discounted Price - Cost
    - Profit% = (Profit / Cost) × 100
    - Loss = Cost - Discounted Price
    - Loss% = (Loss / Cost) × 100
    - Discount = ((Selling Price - Discounted Price) / Selling Price) × 100
    - Discounted Price = Selling Price × (1 - Discount%/100)
    """)

st.markdown("---")
st.caption("💡 Tip: The profit/loss is always calculated based on the discounted price vs cost.")
